import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ingest import load_data
from personas import create_personas
import config

def collaborative_filtering(events, guest_id, bookings, n=config.DEFAULT_RECOMMENDATIONS):
    bookings['date'] = pd.to_datetime(bookings['date'])
    events['date'] = pd.to_datetime(events['date'])
    
    guest_bookings = bookings[bookings['guest_id'] == guest_id]
    if len(guest_bookings) == 0:
        return pd.DataFrame()
    
    guest_dates = guest_bookings['date'].unique()
    guest_events = events[events['date'].isin(guest_dates)]
    
    if len(guest_events) == 0:
        return pd.DataFrame()
    
    user_item = bookings.groupby(['guest_id', 'date']).size().reset_index(name='count')
    user_item = user_item.merge(events[['date', 'event_id']], on='date', how='inner')
    user_item_matrix = user_item.pivot_table(index='guest_id', columns='event_id', values='count', fill_value=0)
    
    if guest_id not in user_item_matrix.index:
        return pd.DataFrame()
    
    user_similarity = cosine_similarity(user_item_matrix.loc[[guest_id]], user_item_matrix)[0]
    sorted_indices = user_similarity.argsort()
    top_indices = sorted_indices[-config.SIMILAR_USERS_COUNT:]
    top_indices = top_indices[::-1]
    similar_users = user_item_matrix.index[top_indices[1:]]
    
    similar_users_events = user_item_matrix.loc[similar_users].sum()
    guest_events_ids = set(guest_events['event_id'].values)
    similar_users_events = similar_users_events[~similar_users_events.index.isin(guest_events_ids)]
    
    top_event_ids = similar_users_events.nlargest(n).index
    return events[events['event_id'].isin(top_event_ids)]

def content_based_filtering(events, guest_id, personas, bookings, n=config.DEFAULT_RECOMMENDATIONS):
    if len(events) == 0:
        return pd.DataFrame()
    
    events_shuffled = events.sample(frac=1, random_state=guest_id).reset_index(drop=True)
    
    guest_persona = personas[personas['guest_id'] == guest_id]['persona_id'].values
    if len(guest_persona) == 0:
        guest_persona = [0]
    
    persona_guests = personas[personas['persona_id'] == guest_persona[0]]['guest_id'].tolist()
    persona_bookings = bookings[bookings['guest_id'].isin(persona_guests)]
    
    if len(persona_bookings) > 0:
        booked_dates = persona_bookings['date'].unique()
        persona_events = events_shuffled[events_shuffled['date'].isin(booked_dates)]
    else:
        return events_shuffled.head(n)
    
    if len(persona_events) == 0:
        return events_shuffled.head(n)
    
    if len(persona_events) == len(events_shuffled):
        return events_shuffled.head(n)
    
    events_text = persona_events['type'] + ' ' + persona_events['name'] + ' ' + persona_events['location']
    
    if events_text.fillna('').str.strip().eq('').all():
        return events_shuffled.head(n)
    
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(events_text.fillna(''))
    
    all_events_text = events_shuffled['type'] + ' ' + events_shuffled['name'] + ' ' + events_shuffled['location']
    all_tfidf = vectorizer.transform(all_events_text.fillna(''))
    
    persona_tfidf = vectorizer.transform(persona_events['type'] + ' ' + persona_events['name'] + ' ' + persona_events['location'])
    persona_mean = persona_tfidf.mean(axis=0)
    persona_mean = np.asarray(persona_mean).reshape(1, -1)
    similarity = cosine_similarity(persona_mean, all_tfidf)[0]
    
    sorted_indices = similarity.argsort()
    top_indices = sorted_indices[-n:]
    top_indices = top_indices[::-1]
    return events_shuffled.iloc[top_indices]

def recommend_events(guest_id, n=config.DEFAULT_RECOMMENDATIONS, start_date=None, end_date=None):
    bookings, events, _ = load_data()
    personas = create_personas(bookings)
    
    events = events.copy()
    events['date'] = pd.to_datetime(events['date'])
    if start_date is None:
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        end_date_default = tomorrow + timedelta(days=config.DEFAULT_RECOMMENDATION_DAYS)
        events = events[(events['date'].dt.date >= tomorrow) & (events['date'].dt.date <= end_date_default)]
    else:
        if end_date is None:
            end_date = start_date + timedelta(days=config.DEFAULT_RECOMMENDATION_DAYS)
        events = events[(events['date'].dt.date >= start_date) & (events['date'].dt.date <= end_date)]
    
    collab_recs = collaborative_filtering(events.copy(), guest_id, bookings, n)
    content_recs = content_based_filtering(events.copy(), guest_id, personas, bookings, n)
    
    if len(collab_recs) > 0 and len(content_recs) > 0:
        result = pd.concat([collab_recs, content_recs]).drop_duplicates(subset=['name']).head(n)
    elif len(collab_recs) > 0:
        result = collab_recs.head(n)
    else:
        result = content_recs.head(n)
    
    return result.sort_values('date')
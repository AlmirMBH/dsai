import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

def recommend_events(events, guest_id, personas, bookings, n=config.DEFAULT_RECOMMENDATIONS):
    events = events.copy()
    events['date'] = pd.to_datetime(events['date'])
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    events = events[events['date'].dt.date >= tomorrow]
    
    collab_recs = collaborative_filtering(events.copy(), guest_id, bookings, n)
    content_recs = content_based_filtering(events.copy(), guest_id, personas, bookings, n)
    
    if len(collab_recs) > 0 and len(content_recs) > 0:
        combined = pd.concat([collab_recs, content_recs]).drop_duplicates(subset=['name'])
        return combined.head(n)
    elif len(collab_recs) > 0:
        return collab_recs.head(n)
    else:
        return content_recs.head(n)


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loading import get_data
from personas import create_personas
import config

def collaborative_filtering(events, guest_id, bookings, n=config.DEFAULT_RECOMMENDATIONS):
    bookings['date'] = pd.to_datetime(bookings['date'])
    bookings['arrival_date'] = pd.to_datetime(bookings['arrival_date'])
    bookings['departure_date'] = pd.to_datetime(bookings['departure_date'])
    events['date'] = pd.to_datetime(events['date'])
    
    guest_bookings = bookings[bookings['guest_id'] == guest_id]
    if len(guest_bookings) == 0:
        return pd.DataFrame()
    
    events_key = events.reset_index().copy()
    events_key['_key'] = 1
    
    guest_bookings_key = guest_bookings[['arrival_date', 'departure_date']].copy()
    guest_bookings_key['_key'] = 1
    merged = events_key.merge(guest_bookings_key, on='_key')
    mask = (merged['date'] >= merged['arrival_date']) & (merged['date'] <= merged['departure_date'])
    guest_events = events[events.index.isin(merged[mask]['index'])].drop_duplicates()
    
    if len(guest_events) == 0:
        return pd.DataFrame()
    
    bookings_key = bookings[['guest_id', 'arrival_date', 'departure_date']].copy()
    bookings_key['_key'] = 1
    merged = events_key.merge(bookings_key, on='_key')
    mask = (merged['date'] >= merged['arrival_date']) & (merged['date'] <= merged['departure_date'])
    user_item = merged[mask][['guest_id', 'id']].drop_duplicates()
    user_item['count'] = 1
    user_item_matrix = user_item.pivot_table(index='guest_id', columns='id', values='count', fill_value=0)
    
    if guest_id not in user_item_matrix.index:
        return pd.DataFrame()
    
    user_similarity = cosine_similarity(user_item_matrix.loc[[guest_id]], user_item_matrix)[0]
    sorted_indices = user_similarity.argsort()
    top_indices = sorted_indices[-config.SIMILAR_USERS_COUNT:]
    top_indices = top_indices[::-1]
    similar_users = user_item_matrix.index[top_indices[1:]]
    
    similar_users_events = user_item_matrix.loc[similar_users].sum()
    guest_events_ids = set(guest_events['id'].values)
    similar_users_events = similar_users_events[~similar_users_events.index.isin(guest_events_ids)]
    
    top_event_ids = similar_users_events.nlargest(n).index
    return events[events['id'].isin(top_event_ids)]

def content_based_filtering(events, guest_id, personas, bookings, n=config.DEFAULT_RECOMMENDATIONS):
    if len(events) == 0:
        return pd.DataFrame()
    
    events_shuffled = events.sample(frac=1, random_state=guest_id).reset_index(drop=True)
    
    guest_persona = personas[personas['guest_id'] == guest_id]['persona_id'].values
    if len(guest_persona) == 0:
        guest_persona = [0]
    
    persona_guests = personas[personas['persona_id'] == guest_persona[0]]['guest_id'].tolist()
    persona_bookings = bookings[bookings['guest_id'].isin(persona_guests)].copy()
    
    if len(persona_bookings) > 0:
        persona_bookings['arrival_date'] = pd.to_datetime(persona_bookings['arrival_date'])
        persona_bookings['departure_date'] = pd.to_datetime(persona_bookings['departure_date'])
        
        events_with_key = events_shuffled.reset_index().copy()
        events_with_key['_key'] = 1
        bookings_with_key = persona_bookings[['arrival_date', 'departure_date']].copy()
        bookings_with_key['_key'] = 1
        
        merged = events_with_key.merge(bookings_with_key, on='_key')
        mask = (merged['date'] >= merged['arrival_date']) & (merged['date'] <= merged['departure_date'])
        persona_events = events_shuffled[events_shuffled.index.isin(merged[mask]['index'])].drop_duplicates()
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
    bookings, events, _, _ = get_data()
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
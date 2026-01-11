import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_ingestion import get_data
from personas import create_personas
import config

def find_events_in_date_ranges(events, date_ranges_df, extra_cols=None):
    """Find events that fall within any of the given date ranges using pandas cross merge."""
    events_reset = events.reset_index().copy()
    columns_to_copy = ['arrival_date', 'departure_date']
    if extra_cols:
        columns_to_copy.extend(extra_cols)
    
    ranges_subset = date_ranges_df[columns_to_copy].copy()
    merged = events_reset.merge(ranges_subset, how='cross')
    mask = (merged['date'] >= merged['arrival_date']) & (merged['date'] <= merged['departure_date'])
    return merged[mask]

def collaborative_filtering(events, guest_id, personas, bookings, number_of_recommendations=config.DEFAULT_RECOMMENDATIONS):
    bookings['date'] = pd.to_datetime(bookings['date'])
    bookings['arrival_date'] = pd.to_datetime(bookings['arrival_date'])
    bookings['departure_date'] = pd.to_datetime(bookings['departure_date'])
    events['date'] = pd.to_datetime(events['date'])
    
    guest_persona = personas[personas['guest_id'] == guest_id]['persona_id'].values
    if len(guest_persona) == 0:
        return pd.DataFrame()
    
    persona_id = guest_persona[0]
    persona_guests = personas[personas['persona_id'] == persona_id]['guest_id'].unique()
    persona_bookings = bookings[bookings['guest_id'].isin(persona_guests)]
    
    guest_bookings = persona_bookings[persona_bookings['guest_id'] == guest_id]
    if len(guest_bookings) == 0:
        return pd.DataFrame()
    
    merged_guest = find_events_in_date_ranges(events, guest_bookings)
    guest_events = events[events.index.isin(merged_guest['index'])].drop_duplicates()
    
    if len(guest_events) == 0:
        return pd.DataFrame()
    
    merged_all = find_events_in_date_ranges(events, persona_bookings, extra_cols=['guest_id'])
    user_item = merged_all[['guest_id', 'id']].drop_duplicates()
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
    
    top_event_ids = similar_users_events.nlargest(number_of_recommendations).index
    return events[events['id'].isin(top_event_ids)]

def content_based_filtering(events, guest_id, personas, bookings, number_of_recommendations=config.DEFAULT_RECOMMENDATIONS):
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
        
        merged = find_events_in_date_ranges(events_shuffled, persona_bookings)
        persona_events = events_shuffled[events_shuffled.index.isin(merged['index'])].drop_duplicates()
    else:
        return events_shuffled.head(number_of_recommendations)
    
    if len(persona_events) == 0:
        return events_shuffled.head(number_of_recommendations)
    
    if len(persona_events) == len(events_shuffled):
        return events_shuffled.head(number_of_recommendations)
    
    events_text = persona_events['type'] + ' ' + persona_events['name'] + ' ' + persona_events['location']
    
    if events_text.fillna('').str.strip().eq('').all():
        return events_shuffled.head(number_of_recommendations)
    
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(events_text.fillna(''))
    
    all_events_text = events_shuffled['type'] + ' ' + events_shuffled['name'] + ' ' + events_shuffled['location']
    all_tfidf = vectorizer.transform(all_events_text.fillna(''))
    
    persona_tfidf = vectorizer.transform(persona_events['type'] + ' ' + persona_events['name'] + ' ' + persona_events['location'])
    persona_mean = persona_tfidf.mean(axis=0)
    persona_mean = np.asarray(persona_mean).reshape(1, -1)
    similarity = cosine_similarity(persona_mean, all_tfidf)[0]
    
    sorted_indices = similarity.argsort()
    top_indices = sorted_indices[-number_of_recommendations:]
    top_indices = top_indices[::-1]  
    return events_shuffled.iloc[top_indices]

def get_bus_route_for_event(event_location, bus_schedules):
    if bus_schedules.empty:
        return "No bus data"
    
    stops_routes = bus_schedules[['stop_name', 'route_id']].drop_duplicates()
    
    for _, row in stops_routes.iterrows():
        stop_name_base = row['stop_name'].replace(', Amsterdam', '')
        if stop_name_base.lower() in event_location.lower():
            return f"{row['route_id']} ({stop_name_base})"
    
    return "Walk / Taxi"

def recommend_events(guest_id, number_of_recommendations=config.DEFAULT_RECOMMENDATIONS, start_date=None, end_date=None):
    bookings, events, _, _, bus_schedules = get_data()
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
    
    collaborative_recommendations = collaborative_filtering(events.copy(), guest_id, personas, bookings, number_of_recommendations)
    content_based_recommendations = content_based_filtering(events.copy(), guest_id, personas, bookings, number_of_recommendations)
    
    if len(collaborative_recommendations) > 0 and len(content_based_recommendations) > 0:
        result = pd.concat([collaborative_recommendations, content_based_recommendations]).drop_duplicates(subset=['name']).head(number_of_recommendations)
    elif len(collaborative_recommendations) > 0:
        result = collaborative_recommendations.head(number_of_recommendations)
    else:
        result = content_based_recommendations.head(number_of_recommendations)
    
    result = result.copy()
    result['bus_route'] = result['location'].apply(lambda loc: get_bus_route_for_event(loc, bus_schedules))
    
    return result.sort_values(['date', 'time'])

#!/usr/bin/env python3

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

np.random.seed(config.RANDOM_STATE)

def generate_web_analytics():
    bookings_file = os.path.join(config.DATASETS_PATH, 'bookings.csv')
    events_file = os.path.join(config.DATASETS_PATH, 'events.csv')
    output_file = os.path.join(config.DATASETS_PATH, 'web_analytics.csv')
    
    print("Generating web analytics...")
    
    bookings = pd.read_csv(bookings_file)
    events = pd.read_csv(events_file)
    
    bookings['date'] = pd.to_datetime(bookings['date'])
    bookings['arrival_date'] = pd.to_datetime(bookings['arrival_date'])
    bookings['departure_date'] = pd.to_datetime(bookings['departure_date'])
    events['date'] = pd.to_datetime(events['date'])
    
    recommendation_start_date = pd.to_datetime(config.RECOMMENDATION_START_DATE)
    control_limit = config.CONTROL_GROUP_PERCENTAGE * 100
    
    analytics = []
    id = 1
    
    for _, booking in bookings.iterrows():
        booking_date = booking['date']
        guest_id = booking['guest_id']
        
        if booking_date < recommendation_start_date:
            continue
        
        if guest_id % 100 < control_limit:
            continue
        
        rec_date = booking_date - timedelta(days=np.random.randint(1, 8))
        rec_date_str = rec_date.strftime('%Y-%m-%d')
        
        mask = (events['date'] >= booking['arrival_date']) & (events['date'] <= booking['departure_date'])
        available_events = events.loc[mask, 'id'].tolist()
        
        if len(available_events) == 0:
            continue
        
        day_of_week = rec_date.weekday()
        is_weekend = day_of_week >= 5
        month = rec_date.month
        is_summer = 6 <= month <= 8
        
        n_recs = np.random.randint(3, 8)
        recommended_events = np.random.choice(available_events, size=min(n_recs, len(available_events)), replace=False)
        
        rooms_booked = booking['rooms_booked']
        rooms_multiplier = 1.0 + (rooms_booked - 1) * 0.25
        
        for event_id in recommended_events:
            base_click_rate = config.BASE_CLICK_RATE
            base_conversion_rate = config.BASE_CONVERSION_RATE * rooms_multiplier
            
            if is_weekend:
                base_click_rate *= 1.3
                base_conversion_rate *= 1.2
            
            if is_summer:
                base_click_rate *= 1.4
                base_conversion_rate *= 1.3
            
            clicked = np.random.random() < base_click_rate
            converted = False
            
            if clicked:
                converted = np.random.random() < base_conversion_rate
            
            analytics.append({
                'id': id,
                'guest_id': int(guest_id),
                'event_id': int(event_id),
                'date_shown': rec_date_str,
                'clicked': int(clicked),
                'converted': int(converted)
            })
            id += 1
    
    df = pd.DataFrame(analytics)
    df.to_csv(output_file, index=False)
    print("Web analytics generation complete.")

if __name__ == '__main__':
    generate_web_analytics()


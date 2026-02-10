#!/usr/bin/env python3
"""
Events Dataset Generator

Generates events.csv for the configured city with:
- Major annual events and festival week from config
- Seasonal patterns (more in summer, weekends)
- Venues from config (EVENTS_VENUES_BY_TYPE)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Set random seed for reproducibility
np.random.seed(config.RANDOM_STATE)

def get_event_time(event_type):
    if event_type in ['conference', 'education']:
        hour = np.random.choice([9, 10, 11])
    elif event_type in ['exhibition', 'arts']:
        hour = np.random.choice([13, 14, 15, 16])
    elif event_type in ['concert', 'music', 'theater', 'comedy']:
        hour = np.random.choice([19, 20, 21])
    elif event_type == 'festival':
        hour = np.random.choice([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    elif event_type == 'sports':
        hour = np.random.choice([9, 10, 11, 14, 15, 16, 17])
    else:
        hour = np.random.choice([14, 15, 16])
    minute = np.random.choice([0, 15, 30, 45])
    return f"{hour:02d}:{minute:02d}"

def generate_events():
    output_file = os.path.join(config.DATASETS_PATH, 'events.csv')
    start_date = datetime.strptime(config.DATASET_START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(config.DATASET_END_DATE, '%Y-%m-%d')
    print("Generating events...")
    events = []
    id = 1
    
    current_date = start_date
    date_range = []
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        day_of_week = date.weekday()
        is_weekend = day_of_week >= 5
        month = date.month
        is_summer = 6 <= month <= 8  # June, July, August
        year = date.year
        
        is_major_event_day = date_str in config.EVENTS_MAJOR_ANNUAL_DATES
        if year in config.EVENTS_ADE_WEEK_START_END_BY_YEAR:
            ade_start = datetime.strptime(config.EVENTS_ADE_WEEK_START_END_BY_YEAR[year]['start'], '%Y-%m-%d')
            ade_end = datetime.strptime(config.EVENTS_ADE_WEEK_START_END_BY_YEAR[year]['end'], '%Y-%m-%d')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            is_ade_week = ade_start <= date_obj <= ade_end
        else:
            is_ade_week = False
        
        # Base probability of events per day
        if is_major_event_day:
            # Major event day - guaranteed major event + additional events
            base_events = 1.5
        elif is_ade_week:
            # ADE week - many events
            base_events = 3.0
        else:
            base_events = 0.8
        
        # Weekend multiplier
        if is_weekend:
            base_events *= 1.8
        
        # Summer multiplier
        if is_summer:
            base_events *= 1.5
        
        # Randomly pick how many events happen a day (like rolling dice, but weighted toward
        # base_events)
        # Poisson can return any non-negative integer (0, 1, 2, 3, 4, 5...), with base_events
        # as the average
        # Example: if base_events=6, most likely values are 4-8, but 0-12+ are all possible
        # max(1, ...) ensures at least 1 event per day (since Poisson could randomly return 0)
        n_events = max(1, int(np.random.poisson(base_events)))
        
        # Add major event if it's a major event day
        if is_major_event_day:
            major = config.EVENTS_MAJOR_ANNUAL_DATES[date_str]
            venue = major['venue']
            location = f"{venue}, {config.CITY_NAME}"
            
            events.append({
                'id': id,
                'date': date_str,
                'time': get_event_time(major['type']),
                'type': major['type'],
                'name': major['name'],
                'location': location,
                'expected_attendance': major['attendance']
            })
            id += 1
            n_events -= 1  # Already added major event
        
        # Generate additional regular events
        for _ in range(n_events):
            event_type = np.random.choice(config.EVENTS_TYPES)
            
            # Select venue based on event type
            if event_type in config.EVENTS_VENUES_BY_TYPE:
                venue = np.random.choice(config.EVENTS_VENUES_BY_TYPE[event_type])
            else:
                venue = np.random.choice(['City Center', 'Various Locations'])
            
            location = f"{venue}, {config.CITY_NAME}"
            
            # Generate event name
            name_pool = config.EVENTS_DISPLAY_NAMES_BY_TYPE.get(event_type, ['Event'])
            event_name = np.random.choice(name_pool)
            
            # Expected attendance based on event type and venue
            attendance_ranges = {
                'concert': (500, 15000),
                'festival': (1000, 50000),
                'conference': (100, 3000),
                'exhibition': (200, 5000),
                'sports': (5000, 55000),
                'education': (50, 1000),
                'music': (200, 5000),
                'arts': (100, 3000),
                'theater': (300, 2000),
                'comedy': (100, 800)
            }
            
            min_att, max_att = attendance_ranges.get(event_type, (100, 1000))
            
            # Adjust for venue size
            if venue in ['Ziggo Dome', 'Johan Cruyff Arena']:
                max_att = min(max_att, 55000)
            elif venue in ['RAI Amsterdam']:
                max_att = min(max_att, 10000)
            
            expected_attendance = max(100, np.random.randint(min_att // 100, max_att // 100 + 1) * 100)
            
            events.append({
                'id': id,
                'date': date_str,
                'time': get_event_time(event_type),
                'type': event_type,
                'name': event_name,
                'location': location,
                'expected_attendance': expected_attendance
            })
            id += 1
    
    df_events = pd.DataFrame(events)
    df_events = df_events.sort_values(['date', 'id'])
    os.makedirs(config.DATASETS_PATH, exist_ok=True)
    df_events.to_csv(output_file, index=False)
    print(f"Generated {len(df_events)} events -> {output_file}")
    return df_events


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate events dataset for configured city')
    parser.parse_args()
    generate_events()


if __name__ == '__main__':
    main()


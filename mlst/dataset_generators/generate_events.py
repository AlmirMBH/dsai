#!/usr/bin/env python3
"""
Amsterdam Events Dataset Generator

Generates realistic events.csv for Amsterdam with:
- Major annual events (King's Day, ADE, Pride, Marathon)
- Seasonal patterns (more in summer, weekends)
- Real Amsterdam venues
- Date range: November 2023 - November 2025
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

# Amsterdam-specific venues
AMSTERDAM_VENUES = {
    'concert': ['Ziggo Dome', 'AFAS Live', 'Paradiso', 'Melkweg', 'Concertgebouw', 'TivoliVredenburg'],
    'festival': ['Vondelpark', 'Westerpark', 'Museumplein', 'Dam Square', 'RAI Amsterdam', 'NDSM Werf'],
    'conference': ['RAI Amsterdam', 'Beurs van Berlage', 'Amsterdam RAI', 'WTC Amsterdam'],
    'exhibition': ['Rijksmuseum', 'Van Gogh Museum', 'Stedelijk Museum', 'Rembrandt House', 'Anne Frank House', 'NEMO Science Museum'],
    'sports': ['Johan Cruyff Arena', 'Olympic Stadium', 'Ziggo Dome', 'AFAS Live'],
    'education': ['University of Amsterdam', 'VU Amsterdam', 'Amsterdam University College', 'Openbare Bibliotheek Amsterdam'],
    'music': ['Paradiso', 'Melkweg', 'Bitterzoet', 'Sugarfactory', 'De School', 'Shelter'],
    'arts': ['Stedelijk Museum', 'Rijksmuseum', 'FOAM Photography Museum', 'EYE Film Museum', 'Moco Museum'],
    'theater': ['Carré Theatre', 'Stadsschouwburg', 'DeLaMar Theatre', 'Royal Theatre'],
    'comedy': ['Boom Chicago', 'Comedy Café', 'Toomler', 'Comedy Theater']
}

EVENT_TYPES = ['concert', 'festival', 'conference', 'exhibition', 'sports', 'education', 'music', 'arts', 'theater', 'comedy']

EVENT_NAMES = {
    'concert': ['Rock Concert', 'Jazz Night', 'Classical Performance', 'Pop Music Show', 'Electronic Music Night', 'Indie Rock Show'],
    'festival': ['Food & Wine Festival', 'Cultural Festival', 'Film Festival', 'Art Festival', 'Music Festival', 'Street Festival'],
    'conference': ['Tech Summit Amsterdam', 'Business Conference', 'Medical Symposium', 'Education Forum', 'Innovation Summit'],
    'exhibition': ['Art Exhibition Opening', 'Photography Show', 'Historical Display', 'Science Exhibition', 'Design Showcase'],
    'sports': ['Ajax Football Match', 'Marathon Race', 'Tennis Tournament', 'Basketball Game', 'Cycling Event', 'Running Event'],
    'education': ['University Open Day', 'Workshop Series', 'Seminar', 'Training Course', 'Educational Fair', 'Lecture Series'],
    'music': ['Live Music Night', 'DJ Set', 'Orchestra Performance', 'Choir Concert', 'Acoustic Session', 'Jazz Session'],
    'arts': ['Theater Performance', 'Dance Show', 'Opera Night', 'Ballet Performance', 'Art Gallery Opening', 'Contemporary Art Show'],
    'theater': ['Drama Play', 'Comedy Show', 'Musical', 'Shakespeare Performance', 'Modern Theater', 'Experimental Theater'],
    'comedy': ['Stand-up Comedy', 'Comedy Night', 'Improv Show', 'Comedy Festival', 'Laugh Out Loud', 'Open Mic Night']
}

# Major annual events in Amsterdam
MAJOR_EVENTS = {
    # 2024
    '2024-04-27': {'type': 'festival', 'name': "King's Day Celebration", 'venue': 'City-wide', 'attendance': 800000},
    '2024-08-03': {'type': 'festival', 'name': 'Amsterdam Pride Canal Parade', 'venue': 'Canal Route', 'attendance': 500000},
    '2024-10-16': {'type': 'music', 'name': 'Amsterdam Dance Event Opening', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2024-10-20': {'type': 'music', 'name': 'Amsterdam Dance Event Closing', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2024-10-20': {'type': 'sports', 'name': 'Amsterdam Marathon', 'venue': 'Olympic Stadium', 'attendance': 45000},
    '2024-12-01': {'type': 'festival', 'name': 'Amsterdam Light Festival Opening', 'venue': 'Canal Route', 'attendance': 100000},
    
    # 2025
    '2025-04-27': {'type': 'festival', 'name': "King's Day Celebration", 'venue': 'City-wide', 'attendance': 800000},
    '2025-08-02': {'type': 'festival', 'name': 'Amsterdam Pride Canal Parade', 'venue': 'Canal Route', 'attendance': 500000},
    '2025-10-15': {'type': 'music', 'name': 'Amsterdam Dance Event Opening', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2025-10-19': {'type': 'music', 'name': 'Amsterdam Dance Event Closing', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2025-10-19': {'type': 'sports', 'name': 'Amsterdam Marathon', 'venue': 'Olympic Stadium', 'attendance': 45000},
    '2025-11-30': {'type': 'festival', 'name': 'Amsterdam Light Festival Opening', 'venue': 'Canal Route', 'attendance': 100000},
}

# ADE week events (multiple events during ADE week)
ADE_WEEKS = {
    2024: {'start': '2024-10-16', 'end': '2024-10-20'},
    2025: {'start': '2025-10-15', 'end': '2025-10-19'}
}


def generate_events():
    output_file = os.path.join(config.DATASETS_PATH, 'events.csv')
    start_date = datetime.strptime(config.DATASET_START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(config.DATASET_END_DATE, '%Y-%m-%d')
    print("Generating events...")
    events = []
    event_id = 1
    
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
        
        is_major_event_day = date_str in MAJOR_EVENTS
        if year in ADE_WEEKS:
            ade_start = datetime.strptime(ADE_WEEKS[year]['start'], '%Y-%m-%d')
            ade_end = datetime.strptime(ADE_WEEKS[year]['end'], '%Y-%m-%d')
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
        
        # Generate number of events (Poisson distribution)
        n_events = max(0, int(np.random.poisson(base_events)))
        
        # Add major event if it's a major event day
        if is_major_event_day:
            major = MAJOR_EVENTS[date_str]
            venue = major['venue']
            location = f"{venue}, Amsterdam"
            
            events.append({
                'event_id': event_id,
                'date': date_str,
                'type': major['type'],
                'name': major['name'],
                'location': location,
                'expected_attendance': major['attendance']
            })
            event_id += 1
            n_events -= 1  # Already added major event
        
        # Generate additional regular events
        for _ in range(n_events):
            event_type = np.random.choice(EVENT_TYPES)
            
            # Select venue based on event type
            if event_type in AMSTERDAM_VENUES:
                venue = np.random.choice(AMSTERDAM_VENUES[event_type])
            else:
                venue = np.random.choice(['City Center', 'Various Locations'])
            
            location = f"{venue}, Amsterdam"
            
            # Generate event name
            name_pool = EVENT_NAMES.get(event_type, ['Event'])
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
            
            expected_attendance = np.random.randint(min_att, max_att)
            
            events.append({
                'event_id': event_id,
                'date': date_str,
                'type': event_type,
                'name': event_name,
                'location': location,
                'expected_attendance': expected_attendance
            })
            event_id += 1
    
    df_events = pd.DataFrame(events)
    df_events = df_events.sort_values(['date', 'event_id'])
    os.makedirs(config.DATASETS_PATH, exist_ok=True)
    df_events.to_csv(output_file, index=False)
    print(f"Generated {len(df_events)} events -> {output_file}")
    return df_events


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate Amsterdam events dataset')
    parser.parse_args()
    generate_events()


if __name__ == '__main__':
    main()


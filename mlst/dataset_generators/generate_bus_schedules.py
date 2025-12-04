#!/usr/bin/env python3
"""
Amsterdam Bus Schedules Dataset Generator

Generates realistic bus_schedules.csv for Amsterdam GVB routes with:
- Real GVB routes and stops
- Time-of-day included
- Realistic schedule patterns (more trips on weekdays)
- Operating hours: 05:30 - 00:30
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

# Real GVB bus routes in Amsterdam
GVB_ROUTES = [
    {
        'route_id': 'R015',
        'name': 'Line 15',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'DAM', 'stop_name': 'Dam'},
            {'stop_id': 'LEI', 'stop_name': 'Leidseplein'},
            {'stop_id': 'MUS', 'stop_name': 'Museumplein'},
            {'stop_id': 'VON', 'stop_name': 'Vondelpark'}
        ]
    },
    {
        'route_id': 'R018',
        'name': 'Line 18',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'DAM', 'stop_name': 'Dam'},
            {'stop_id': 'LEI', 'stop_name': 'Leidseplein'},
            {'stop_id': 'VON', 'stop_name': 'Vondelpark'},
            {'stop_id': 'WES', 'stop_name': 'Westerpark'}
        ]
    },
    {
        'route_id': 'R021',
        'name': 'Line 21',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'DAM', 'stop_name': 'Dam'},
            {'stop_id': 'RAI', 'stop_name': 'RAI Amsterdam'},
            {'stop_id': 'ZUI', 'stop_name': 'Amsterdam Zuid'},
            {'stop_id': 'SCH', 'stop_name': 'Schiphol Airport'}
        ]
    },
    {
        'route_id': 'R022',
        'name': 'Line 22',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'WES', 'stop_name': 'Westerpark'},
            {'stop_id': 'SLT', 'stop_name': 'Sloterdijk'},
            {'stop_id': 'OSD', 'stop_name': 'Osdorp'}
        ]
    },
    {
        'route_id': 'R024',
        'name': 'Line 24',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'OLY', 'stop_name': 'Olympic Stadium'},
            {'stop_id': 'ZUI', 'stop_name': 'Amsterdam Zuid'}
        ]
    },
    {
        'route_id': 'R026',
        'name': 'Line 26',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'ZUI', 'stop_name': 'Amsterdam Zuid'},
            {'stop_id': 'SCH', 'stop_name': 'Schiphol Airport'}
        ]
    },
    {
        'route_id': 'R048',
        'name': 'Line 48',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'REM', 'stop_name': 'Rembrandtplein'},
            {'stop_id': 'MUS', 'stop_name': 'Museumplein'},
            {'stop_id': 'VON', 'stop_name': 'Vondelpark'}
        ]
    },
    {
        'route_id': 'R065',
        'name': 'Line 65',
        'stops': [
            {'stop_id': 'CS', 'stop_name': 'Centraal Station'},
            {'stop_id': 'DAM', 'stop_name': 'Dam'},
            {'stop_id': 'REM', 'stop_name': 'Rembrandtplein'},
            {'stop_id': 'WAT', 'stop_name': 'Waterlooplein'}
        ]
    }
]

# Operating hours
OPERATING_HOURS = {
    'start': 5,  # 05:30
    'end': 0     # 00:30 (next day)
}

# Schedule patterns (frequency in minutes)
SCHEDULE_PATTERNS = {
    'weekday': {
        'peak_morning': (7, 9, 7),      # 07:00-09:00, every 7 minutes
        'midday': (9, 17, 12),          # 09:00-17:00, every 12 minutes
        'peak_evening': (17, 19, 8),    # 17:00-19:00, every 8 minutes
        'evening': (19, 23, 15),        # 19:00-23:00, every 15 minutes
        'late_night': (23, 0, 25)       # 23:00-00:30, every 25 minutes
    },
    'weekend': {
        'morning': (6, 10, 15),         # 06:00-10:00, every 15 minutes
        'midday': (10, 20, 12),         # 10:00-20:00, every 12 minutes
        'evening': (20, 23, 15),        # 20:00-23:00, every 15 minutes
        'late_night': (23, 0, 30)       # 23:00-00:30, every 30 minutes
    }
}


def generate_bus_schedules():
    output_file = os.path.join(config.DATASETS_PATH, 'bus_schedules.csv')
    start_date = datetime.strptime(config.DATASET_START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(config.DATASET_END_DATE, '%Y-%m-%d')
    print("Generating bus schedules...")
    schedules = []
    trip_id = 1
    
    current_date = start_date
    date_range = []
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        day_of_week = date.weekday()
        is_weekend = day_of_week >= 5
        
        patterns = SCHEDULE_PATTERNS['weekend' if is_weekend else 'weekday']
        time_slots = []
        for pattern_name, (start_hour, end_hour, frequency) in patterns.items():
            current_hour = start_hour
            current_minute = 30 if start_hour == OPERATING_HOURS['start'] else 0
            while True:
                if end_hour == 0:
                    if current_hour >= 23 and current_minute >= 30:
                        break
                else:
                    if current_hour >= end_hour:
                        break
                time_str = f"{current_hour:02d}:{current_minute:02d}"
                time_slots.append(time_str)
                current_minute += frequency
                if current_minute >= 60:
                    current_minute -= 60
                    current_hour += 1
                    if current_hour >= 24:
                        current_hour = 0
        
        # Generate trips for each route
        for route in GVB_ROUTES:
            for time_slot in time_slots:
                # Each trip visits all stops in sequence
                for stop_idx, stop_info in enumerate(route['stops']):
                    # Calculate arrival time at this stop (add travel time)
                    # Assume ~3-5 minutes between stops
                    arrival_minutes = int(time_slot.split(':')[1]) + (stop_idx * 4)
                    arrival_hours = int(time_slot.split(':')[0])
                    
                    if arrival_minutes >= 60:
                        arrival_minutes -= 60
                        arrival_hours += 1
                        if arrival_hours >= 24:
                            arrival_hours = 0
                    
                    arrival_time = f"{arrival_hours:02d}:{arrival_minutes:02d}"
                    
                    schedules.append({
                        'trip_id': trip_id,
                        'date': date_str,
                        'time': arrival_time,
                        'route_id': route['route_id'],
                        'stop_id': stop_info['stop_id'],
                        'stop_name': f"{stop_info['stop_name']}, Amsterdam"
                    })
                trip_id += 1
    
    df_schedules = pd.DataFrame(schedules)
    df_schedules = df_schedules.sort_values(['date', 'route_id', 'time', 'stop_id'])
    os.makedirs(config.DATASETS_PATH, exist_ok=True)
    df_schedules.to_csv(output_file, index=False)
    print(f"Generated {len(df_schedules)} schedule entries -> {output_file}")
    return df_schedules


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate Amsterdam bus schedules dataset')
    parser.parse_args()
    generate_bus_schedules()


if __name__ == '__main__':
    main()
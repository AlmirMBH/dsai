#!/usr/bin/env python3
"""
Bus Schedules Dataset Generator

Generates bus_schedules.csv for the configured city with:
- Routes and stops from config (BUS_ROUTES)
- Time-of-day included
- Schedule patterns (weekday vs weekend)
- Operating hours from config
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

def generate_bus_schedules():
    output_file = os.path.join(config.DATASETS_PATH, 'bus_schedules.csv')
    start_date = datetime.strptime(config.DATASET_START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(config.DATASET_END_DATE, '%Y-%m-%d')
    print("Generating bus schedules...")
    schedules = []
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
        
        patterns = config.BUS_SCHEDULE_PATTERNS_WEEKDAY_WEEKEND['weekend' if is_weekend else 'weekday']
        time_slots = []
        for pattern_name, (start_hour, end_hour, frequency) in patterns.items():
            current_hour = start_hour
            current_minute = 30 if start_hour == config.BUS_OPERATING_HOURS_START_END['start'] else 0
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
        
        # Add random 5% variance to daily trips
        time_slots = np.random.choice(time_slots, size=int(len(time_slots) * np.random.uniform(0.95, 1.05)))

        # Generate trips for each route
        for route in config.BUS_ROUTES:
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
                        'id': id,
                        'date': date_str,
                        'time': arrival_time,
                        'route_id': route['route_id'],
                        'stop_id': stop_info['stop_id'],
                        'stop_name': f"{stop_info['stop_name']}, {config.CITY_NAME}"
                    })
                id += 1
    
    df_schedules = pd.DataFrame(schedules)
    df_schedules = df_schedules.sort_values(['date', 'route_id', 'time', 'stop_id'])
    os.makedirs(config.DATASETS_PATH, exist_ok=True)
    df_schedules.to_csv(output_file, index=False)
    print(f"Generated {len(df_schedules)} schedule entries -> {output_file}")
    return df_schedules


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate bus schedules dataset for configured city')
    parser.parse_args()
    generate_bus_schedules()


if __name__ == '__main__':
    main()
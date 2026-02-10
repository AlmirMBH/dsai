#!/usr/bin/env python3
"""
Bookings Dataset Generator

Generates bookings.csv for the configured city with:
- Addresses from config (street names, districts, city, country)
- Correlations with events and weather
- 50-200 bookings per day
- Guests from around the world
"""

import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Set random seed for reproducibility
np.random.seed(config.RANDOM_STATE)

def generate_accommodations(n_accommodations=None):
    if n_accommodations is None:
        n_accommodations = config.DATASET_N_ACCOMMODATIONS
    """Generate accommodation data with addresses from config (city, streets, districts)."""
    accommodations = []
    for i in range(1, n_accommodations + 1):
        acc_type = np.random.choice(config.BOOKINGS_ACCOMMODATION_TYPES)
        cap_type = np.random.choice(config.BOOKINGS_CAPACITY_TYPES)
        stars = np.random.choice([3, 4, 5], p=[0.3, 0.5, 0.2])
        acc_name = np.random.choice(config.BOOKINGS_ACCOMMODATION_NAMES)
        if i <= len(config.BOOKINGS_ACCOMMODATION_NAMES):
            acc_name = config.BOOKINGS_ACCOMMODATION_NAMES[i-1]
        else:
            acc_name = f"{acc_name} {i}"
        
        street = np.random.choice(config.BOOKINGS_STREET_NAMES)
        district = np.random.choice(config.BOOKINGS_DISTRICTS)
        house_number = np.random.randint(1, 300)
        address = f"{house_number} {street}, {district}, {config.CITY_NAME}, {config.COUNTRY_NAME}"
        
        accommodations.append({
            'accommodation_id': i,
            'accommodation_code': 1000 + i,
            'accommodation_name': acc_name,
            'address': address,
            'stars': stars,
            'capacity_type': cap_type,
            'accommodation_units': np.random.randint(10, 200),
            'type': acc_type
        })
    return pd.DataFrame(accommodations)




def create_booking(guest_id, guest_info, booking_date, accommodations_df, booking_id):
    """Create a single booking."""
    acc = accommodations_df.sample(1).iloc[0]
    
    days_until_arrival = np.random.randint(0, 90)
    arrival_date = booking_date + timedelta(days=days_until_arrival)
    stay_nights = np.random.randint(1, 14)
    departure_date = arrival_date + timedelta(days=stay_nights)
    
    rooms_booked = np.random.randint(1, 5)
    number_of_guests = np.random.choice(['single', 'couple', 'family', 'group'], 
                                      p=[0.2, 0.4, 0.3, 0.1])
    
    base_rate = 50 + (acc['stars'] * 20) + np.random.randint(-20, 50)
    average_daily_rate = int(max(30, base_rate) * 100 * np.random.uniform(0.9, 1.1))
    revenue_available_room = (average_daily_rate * stay_nights) // rooms_booked
    
    created_at = booking_date - timedelta(days=np.random.randint(0, 30))
    updated_at = created_at + timedelta(days=np.random.randint(0, 5))
    deleted_at = None if np.random.random() > 0.05 else updated_at + timedelta(days=np.random.randint(1, 30))
    
    return {
        'id': booking_id,
        'uuid': str(uuid.uuid4()),
        'accommodation_id': acc['accommodation_id'],
        'accommodation_code': acc['accommodation_code'],
        'accommodation_name': acc['accommodation_name'],
        'address': acc['address'],
        'stars': acc['stars'],
        'capacity_type': acc['capacity_type'],
        'accommodation_units': acc['accommodation_units'],
        'type': acc['type'],
        'guest_id': guest_id,
        'first_name': guest_info['first_name'],
        'last_name': guest_info['last_name'],
        'email': guest_info['email'],
        'age': guest_info['age'],
        'country_id': guest_info['country_id'],
        'date': booking_date.strftime('%Y-%m-%d'),
        'rooms_booked': rooms_booked,
        'number_of_guests': number_of_guests,
        'average_daily_rate': average_daily_rate,
        'revenue_available_room': revenue_available_room,
        'arrival_date': arrival_date.strftime('%Y-%m-%d'),
        'departure_date': departure_date.strftime('%Y-%m-%d'),
        'guest_country': guest_info['country'],
        'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'deleted_at': deleted_at.strftime('%Y-%m-%d %H:%M:%S') if deleted_at else None
    }

def calculate_booking_multiplier(date_str, events_by_date, weather_by_date):
    """Calculate booking multiplier based on events and weather."""
    multiplier = 1.0
    
    # Event impact: more bookings during major events
    if date_str in events_by_date:
        attendance = events_by_date[date_str]
        # Scale: 0.1% of event attendance might book accommodation
        # Major events boost bookings by 20-30%
        if attendance > config.EVENT_ATTENDANCE_MAX:
            multiplier += 0.25
        elif attendance > config.EVENT_ATTENDANCE_MAX / 2:
            multiplier += 0.15
        elif attendance > config.EVENT_ATTENDANCE_MAX / 10:
            multiplier += 0.10
        else:
            multiplier += 0.05
    
    # Weather impact
    if date_str in weather_by_date:
        weather = weather_by_date[date_str]
        weather_cat = weather.get('weather_category', 'cloudy')
        temp_max = weather.get('temperature_max', 150) / 10.0  # Convert from *10
        
        # Good weather boosts bookings
        if weather_cat == 'sunny' and temp_max > 18:
            multiplier += 0.15
        elif weather_cat == 'sunny':
            multiplier += 0.10
        elif weather_cat == 'partly_cloudy':
            multiplier += 0.05
        elif weather_cat == 'rainy':
            multiplier -= 0.05
        elif weather_cat == 'snowy':
            multiplier -= 0.10
    
    # Weekend boost
    date = datetime.strptime(date_str, '%Y-%m-%d')
    if date.weekday() >= 5:  # Weekend
        multiplier += 0.10
    
    # Summer boost
    if 6 <= date.month <= 8:  # June, July, August
        multiplier += 0.15
    
    return max(0.5, multiplier)  # Ensure minimum 50% of base


def generate_bookings(accommodations_df):
    events_file = os.path.join(config.DATASETS_PATH, 'events.csv')
    weather_file = os.path.join(config.DATASETS_PATH, 'weather.csv')
    output_file = os.path.join(config.DATASETS_PATH, 'bookings.csv')
    start_date = datetime.strptime(config.DATASET_START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(config.DATASET_END_DATE, '%Y-%m-%d')
    print("Generating bookings...")
    bookings = []
    
    if os.path.exists(events_file):
        df_events = pd.read_csv(events_file)
        events_by_date = df_events.groupby('date')['expected_attendance'].sum().to_dict()
    else:
        events_by_date = {}
    
    if os.path.exists(weather_file):
        df_weather = pd.read_csv(weather_file)
        weather_by_date = df_weather.set_index('date').to_dict('index')
    else:
        weather_by_date = {}
    
    current_date = start_date
    date_range = []
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    booking_id = 1
    guest_id_counter = 1
    guest_pool = {}  # Reuse guest IDs for repeat visitors
    
    # Define deterministic control group assignment
    recommendation_start_date = datetime.strptime(config.RECOMMENDATION_START_DATE, '%Y-%m-%d')
    control_limit = config.CONTROL_GROUP_PERCENTAGE * 100
    
    base_bookings_per_day = config.DATASET_BASE_BOOKINGS_PER_DAY
    
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        
        # Calculate booking multiplier
        multiplier = calculate_booking_multiplier(date_str, events_by_date, weather_by_date)
        n_bookings_today = int(base_bookings_per_day * multiplier * np.random.uniform(0.85, 1.15)) # 15%
        n_bookings_today = np.clip(n_bookings_today, config.DATASET_MIN_BOOKINGS_PER_DAY, config.DATASET_MAX_BOOKINGS_PER_DAY)
        
        for _ in range(n_bookings_today):
            # Generate or reuse guest information
            # Dynamic repeat probability: higher for treatment guests after recommendations start
            is_after_recommendations = date >= recommendation_start_date
            
            # Base repeat probability
            repeat_probability = config.BASE_REPEAT_PROBABILITY
            
            reuse_guest = False
            if np.random.random() < repeat_probability and len(guest_pool) > 0:  # Dynamic chance of repeat guest
                guest_id = np.random.choice(list(guest_pool.keys()))
                guest_info = guest_pool[guest_id]
                
                # Boost repeat probability for treatment guests after recommendations start
                if is_after_recommendations:
                    is_treatment_guest = not (guest_id % 100 < control_limit)
                    if is_treatment_guest:
                        # Treatment guests: keep reuse (recommendations help retention)
                        reuse_guest = True
                    else:
                        # Control guests: lower retention (no recommendations)
                        if np.random.random() < config.CONTROL_RETENTION_DROP:
                            reuse_guest = False
                        else:
                            reuse_guest = True
                else:
                    reuse_guest = True
            
            if reuse_guest:
                # Reuse existing guest (already set above)
                pass
            else:
                # New guest
                first_name = np.random.choice(config.BOOKINGS_GUEST_FIRST_NAMES_POOL)
                last_name = np.random.choice(config.BOOKINGS_GUEST_LAST_NAMES_POOL)
                email = f"{first_name.lower()}.{last_name.lower()}@{np.random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])}"
                age = np.random.randint(18, 80)
                guest_country = np.random.choice(config.BOOKINGS_GUEST_COUNTRIES)
                country_id = config.BOOKINGS_GUEST_COUNTRIES.index(guest_country) + 1
                guest_id = guest_id_counter
                guest_info = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'age': age,
                    'country': guest_country,
                    'country_id': country_id
                }
                guest_pool[guest_id] = guest_info
                guest_id_counter += 1
            
            booking = create_booking(guest_id, guest_info, date, accommodations_df, booking_id)
            bookings.append(booking)
            booking_id += 1
    
    df_bookings = pd.DataFrame(bookings)
    os.makedirs(config.DATASETS_PATH, exist_ok=True)
    df_bookings.to_csv(output_file, index=False)
    print(f"Generated {len(df_bookings)} bookings -> {output_file}")
    return df_bookings


def generate_additional_bookings(accommodations_df, existing_bookings_df):
    """Generate additional bookings for converted guests from web_analytics."""
    web_analytics_file = os.path.join(config.DATASETS_PATH, 'web_analytics.csv')
    if not os.path.exists(web_analytics_file):
        return []
    
    web_analytics = pd.read_csv(web_analytics_file)
    web_analytics['date_shown'] = pd.to_datetime(web_analytics['date_shown'])    
    converted = web_analytics[web_analytics['converted'] == 1].copy()
    
    if len(converted) == 0:
        return []
    
    converted['conversion_prob'] = config.CONVERSION_BOOST_RATE
    
    mask = np.random.random(len(converted)) < converted['conversion_prob']
    converted = converted[mask].drop_duplicates(subset='guest_id')
    
    guest_info_map = {}
    for _, booking in existing_bookings_df.iterrows():
        guest_id = booking['guest_id']
        if guest_id not in guest_info_map:
            guest_info_map[guest_id] = {
                'first_name': booking['first_name'],
                'last_name': booking['last_name'],
                'email': booking['email'],
                'age': booking['age'],
                'country': booking['guest_country'],
                'country_id': booking['country_id']
            }
    
    additional_bookings = []
    booking_id = existing_bookings_df['id'].max() + 1
    
    for _, rec in converted.iterrows():
        guest_id = rec['guest_id']
        if guest_id not in guest_info_map:
            continue
        
        booking_date = rec['date_shown'] + timedelta(days=np.random.randint(1, 30))
        guest_info = guest_info_map[guest_id]
        booking = create_booking(guest_id, guest_info, booking_date, accommodations_df, booking_id)
        additional_bookings.append(booking)
        booking_id += 1
    
    return additional_bookings


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate bookings dataset for configured city')
    parser.add_argument(
        '--n-accommodations',
        type=int,
        default=config.DATASET_N_ACCOMMODATIONS,
        help=f'Number of accommodations (default: {config.DATASET_N_ACCOMMODATIONS})'
    )
    
    args = parser.parse_args()
    accommodations_df = generate_accommodations(args.n_accommodations)
    generate_bookings(accommodations_df)


if __name__ == '__main__':
    main()


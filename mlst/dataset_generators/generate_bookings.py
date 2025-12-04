#!/usr/bin/env python3
"""
Amsterdam Bookings Dataset Generator

Generates realistic bookings.csv for Amsterdam with:
- Amsterdam addresses only
- Correlations with events and weather
- 50-200 bookings per day
- Guests from around the world
- Date range: November 2023 - November 2025
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

# Sample data pools
FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
    'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
    'Kenneth', 'Carol', 'Kevin', 'Amanda', 'Brian', 'Dorothy', 'George', 'Melissa',
    'Timothy', 'Deborah', 'Ronald', 'Stephanie', 'Jason', 'Rebecca', 'Edward', 'Sharon'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
    'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris', 'Sanchez',
    'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
    'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams',
    'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts'
]

ACCOMMODATION_TYPES = ['hotel', 'hostel', 'apartment', 'resort', 'villa', 'bed_and_breakfast']
CAPACITY_TYPES = ['room', 'bed', 'suite', 'apartment', 'villa', 'house']
GUEST_COUNTRIES = [
    'United States', 'United Kingdom', 'Germany', 'France', 'Italy', 'Spain',
    'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Canada', 'Australia',
    'Japan', 'China', 'Brazil', 'Mexico', 'Argentina', 'South Africa', 'India', 'Russia'
]

# Amsterdam-specific accommodation names
AMSTERDAM_ACCOMMODATION_NAMES = [
    'Grand Hotel Amsterdam', 'Canal View Hotel', 'Rijksmuseum Hotel', 'Dam Square Hotel',
    'Vondelpark Hotel', 'Leidseplein Hotel', 'Jordaan Boutique Hotel', 'Museum Quarter Hotel',
    'Central Station Hotel', 'Anne Frank Hotel', 'Red Light District Hotel', 'Westerpark Hotel',
    'Amsterdam Marriott', 'Hilton Amsterdam', 'NH Collection Amsterdam', 'Park Plaza Amsterdam',
    'Hotel Okura Amsterdam', 'Conservatorium Hotel', 'Pulitzer Amsterdam', 'Waldorf Astoria Amsterdam'
]

# Real Amsterdam street names
AMSTERDAM_STREETS = [
    'Damrak', 'Kalverstraat', 'Nieuwendijk', 'Leidsestraat', 'Rokin', 'Singel',
    'Herengracht', 'Keizersgracht', 'Prinsengracht', 'Jordaan', 'Rozengracht',
    'Overtoom', 'Vondelstraat', 'P.C. Hooftstraat', 'Van Baerlestraat', 'Museumplein',
    'Leidseplein', 'Rembrandtplein', 'Waterlooplein', 'Dam Square', 'Spui',
    'Nieuwezijds Voorburgwal', 'Oudezijds Voorburgwal', 'Warmoesstraat', 'Zeedijk'
]

AMSTERDAM_DISTRICTS = [
    'Centrum', 'Jordaan', 'De Pijp', 'Oud-Zuid', 'Oud-West', 'Westerpark',
    'Oost', 'Noord', 'Zuid', 'Nieuw-West'
]


def generate_accommodations(n_accommodations=None):
    if n_accommodations is None:
        n_accommodations = config.DATASET_N_ACCOMMODATIONS
    """Generate accommodation data with Amsterdam addresses."""
    accommodations = []
    for i in range(1, n_accommodations + 1):
        acc_type = np.random.choice(ACCOMMODATION_TYPES)
        cap_type = np.random.choice(CAPACITY_TYPES)
        stars = np.random.choice([3, 4, 5], p=[0.3, 0.5, 0.2])
        acc_name = np.random.choice(AMSTERDAM_ACCOMMODATION_NAMES)
        if i <= len(AMSTERDAM_ACCOMMODATION_NAMES):
            acc_name = AMSTERDAM_ACCOMMODATION_NAMES[i-1]
        else:
            acc_name = f"{acc_name} {i}"
        
        street = np.random.choice(AMSTERDAM_STREETS)
        district = np.random.choice(AMSTERDAM_DISTRICTS)
        house_number = np.random.randint(1, 300)
        address = f"{house_number} {street}, {district}, Amsterdam, Netherlands"
        
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




def calculate_booking_multiplier(date_str, events_by_date, weather_by_date):
    """Calculate booking multiplier based on events and weather."""
    multiplier = 1.0
    
    # Event impact: more bookings during major events
    if date_str in events_by_date:
        attendance = events_by_date[date_str]
        # Scale: 0.1% of event attendance might book accommodation
        # Major events (>100k attendance) boost bookings by 20-30%
        if attendance > 100000:
            multiplier += 0.25
        elif attendance > 50000:
            multiplier += 0.15
        elif attendance > 10000:
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
    
    base_bookings_per_day = config.DATASET_BASE_BOOKINGS_PER_DAY
    
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        
        # Calculate booking multiplier
        multiplier = calculate_booking_multiplier(date_str, events_by_date, weather_by_date)
        n_bookings_today = int(base_bookings_per_day * multiplier)
        n_bookings_today = np.clip(n_bookings_today, config.DATASET_MIN_BOOKINGS_PER_DAY, config.DATASET_MAX_BOOKINGS_PER_DAY)
        
        for _ in range(n_bookings_today):
            # Select random accommodation
            acc = accommodations_df.sample(1).iloc[0]
            
            # Generate or reuse guest information
            if np.random.random() < 0.3:  # 30% chance of repeat guest
                guest_id = np.random.choice(list(guest_pool.keys()))
                guest_info = guest_pool[guest_id]
                first_name = guest_info['first_name']
                last_name = guest_info['last_name']
                email = guest_info['email']
                age = guest_info['age']
                guest_country = guest_info['country']
                country_id = guest_info['country_id']
            else:
                # New guest
                first_name = np.random.choice(FIRST_NAMES)
                last_name = np.random.choice(LAST_NAMES)
                email = f"{first_name.lower()}.{last_name.lower()}@{np.random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])}"
                age = np.random.randint(18, 80)
                guest_country = np.random.choice(GUEST_COUNTRIES)
                country_id = GUEST_COUNTRIES.index(guest_country) + 1
                guest_id = guest_id_counter
                guest_pool[guest_id] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'age': age,
                    'country': guest_country,
                    'country_id': country_id
                }
                guest_id_counter += 1
            
            # Generate booking dates
            booking_date = date
            # Arrival can be same day or up to 90 days in future
            days_until_arrival = np.random.randint(0, 90)
            arrival_date = booking_date + timedelta(days=days_until_arrival)
            # Stay duration: 1-14 nights
            stay_nights = np.random.randint(1, 14)
            departure_date = arrival_date + timedelta(days=stay_nights)
            
            # Generate booking details
            rooms_booked = np.random.randint(1, 5)
            number_of_guests = np.random.choice(['single', 'couple', 'family', 'group'], 
                                              p=[0.2, 0.4, 0.3, 0.1])
            
            # Generate pricing (based on stars and type)
            base_rate = 50 + (acc['stars'] * 20) + np.random.randint(-20, 50)
            average_daily_rate = max(30, base_rate) * 100  # Store as integer (price * 100)
            
            # Revenue per available room
            revenue_available_room = (average_daily_rate * stay_nights) // rooms_booked
            
            # Timestamps
            created_at = booking_date - timedelta(days=np.random.randint(0, 30))
            updated_at = created_at + timedelta(days=np.random.randint(0, 5))
            deleted_at = None if np.random.random() > 0.05 else updated_at + timedelta(days=np.random.randint(1, 30))
            
            booking = {
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
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'age': age,
                'country_id': country_id,
                'date': booking_date.strftime('%Y-%m-%d'),
                'rooms_booked': rooms_booked,
                'number_of_guests': number_of_guests,
                'average_daily_rate': average_daily_rate,
                'revenue_available_room': revenue_available_room,
                'arrival_date': arrival_date.strftime('%Y-%m-%d'),
                'departure_date': departure_date.strftime('%Y-%m-%d'),
                'guest_country': guest_country,
                'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'deleted_at': deleted_at.strftime('%Y-%m-%d %H:%M:%S') if deleted_at else None
            }
            
            bookings.append(booking)
            booking_id += 1
    
    df_bookings = pd.DataFrame(bookings)
    os.makedirs(config.DATASETS_PATH, exist_ok=True)
    df_bookings.to_csv(output_file, index=False)
    print(f"Generated {len(df_bookings)} bookings -> {output_file}")
    return df_bookings


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate Amsterdam bookings dataset')
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


#!/usr/bin/env python3
"""
Amsterdam Weather Dataset Generator

Generates realistic weather.csv for Amsterdam with:
- Maritime climate patterns
- Seasonal temperature variations
- Realistic precipitation patterns
- Humidity included
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

# Amsterdam climate parameters
AMSTERDAM_CLIMATE = {
    'winter': {'avg_temp': 4, 'temp_range': (-2, 10), 'rain_prob': 0.45, 'humidity': (80, 95)},
    'spring': {'avg_temp': 10, 'temp_range': (3, 18), 'rain_prob': 0.30, 'humidity': (70, 85)},
    'summer': {'avg_temp': 19, 'temp_range': (12, 28), 'rain_prob': 0.25, 'humidity': (65, 80)},
    'autumn': {'avg_temp': 12, 'temp_range': (5, 18), 'rain_prob': 0.40, 'humidity': (75, 90)}
}

WEATHER_CATEGORIES = ['sunny', 'partly_cloudy', 'cloudy', 'rainy', 'windy', 'foggy', 'snowy']


def get_season(date):
    """Determine season based on date."""
    month = date.month
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'


def generate_weather():
    output_file = os.path.join(config.DATASETS_PATH, 'weather.csv')
    start_date = datetime.strptime(config.DATASET_START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(config.DATASET_END_DATE, '%Y-%m-%d')
    print("Generating weather...")
    weather = []
    
    current_date = start_date
    date_range = []
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    # Track previous day's weather for continuity
    prev_temp_max = None
    prev_temp_min = None
    
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        season = get_season(date)
        climate = AMSTERDAM_CLIMATE[season]
        
        # Day of year for seasonal variation
        day_of_year = date.timetuple().tm_yday
        
        # Base temperature with seasonal sine wave
        # Peak around July 15 (day 196), trough around January 15 (day 15)
        seasonal_factor = np.sin(2 * np.pi * (day_of_year - 15) / 365)
        base_temp = climate['avg_temp'] + 7 * seasonal_factor
        
        # Add daily variation
        temp_variation = np.random.normal(0, 3)
        temp_max = base_temp + temp_variation + np.random.uniform(2, 6)
        temp_min = base_temp + temp_variation - np.random.uniform(2, 6)
        
        # Ensure min < max
        if temp_min >= temp_max:
            temp_min = temp_max - np.random.uniform(3, 8)
        
        # Clamp to realistic ranges for Amsterdam
        temp_max = np.clip(temp_max, climate['temp_range'][0], climate['temp_range'][1])
        temp_min = np.clip(temp_min, climate['temp_range'][0] - 3, climate['temp_range'][1] - 5)
        
        # Add continuity (smooth transitions)
        if prev_temp_max is not None:
            temp_max = 0.7 * temp_max + 0.3 * prev_temp_max
            temp_min = 0.7 * temp_min + 0.3 * prev_temp_min
        
        prev_temp_max = temp_max
        prev_temp_min = temp_min
        
        # Convert to integers (temperature * 10)
        temp_max_int = int(round(temp_max * 10))
        temp_min_int = int(round(temp_min * 10))
        
        # Precipitation
        rain_prob = climate['rain_prob']
        is_raining = np.random.random() < rain_prob
        
        if is_raining:
            # Rain amount (mm) - heavier in autumn/winter
            if season in ['autumn', 'winter']:
                precipitation = np.random.randint(2, 25)
            else:
                precipitation = np.random.randint(1, 15)
            weather_category = 'rainy'
        else:
            precipitation = 0
            # Determine weather category based on temperature and season
            if temp_max > 20:
                weather_category = np.random.choice(['sunny', 'partly_cloudy'], p=[0.5, 0.5])
            elif temp_max < 5:
                # Winter weather
                if np.random.random() < 0.1:  # 10% chance of snow
                    weather_category = 'snowy'
                    precipitation = np.random.randint(1, 10)
                else:
                    weather_category = np.random.choice(['cloudy', 'foggy', 'windy'], p=[0.5, 0.3, 0.2])
            else:
                # Moderate temperatures
                weather_category = np.random.choice(['cloudy', 'partly_cloudy', 'sunny', 'windy'], 
                                                  p=[0.4, 0.3, 0.2, 0.1])
        
        # Humidity (higher when raining, lower when sunny)
        if weather_category == 'rainy':
            humidity = np.random.randint(climate['humidity'][0], climate['humidity'][1])
        elif weather_category == 'sunny':
            humidity = np.random.randint(50, climate['humidity'][1] - 10)
        else:
            humidity = np.random.randint(climate['humidity'][0] - 10, climate['humidity'][1])
        
        weather.append({
            'date': date_str,
            'temperature_max': temp_max_int,
            'temperature_min': temp_min_int,
            'weather_category': weather_category,
            'precipitation': precipitation,
            'humidity': humidity
        })
    
    df_weather = pd.DataFrame(weather)
    os.makedirs(config.DATASETS_PATH, exist_ok=True)
    df_weather.to_csv(output_file, index=False)
    print(f"Generated {len(df_weather)} weather dataset -> {output_file}")
    return df_weather


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate Amsterdam weather dataset')
    parser.parse_args()
    generate_weather()


if __name__ == '__main__':
    main()
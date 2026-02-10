#!/usr/bin/env python3
"""
Weather Dataset Generator

Generates realistic weather.csv for the configured city with:
- Seasonal climate from config (WEATHER_SEASONAL_PARAMS)
- Temperature and precipitation patterns
- Humidity included
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
        climate = config.WEATHER_SEASONAL_PARAMS[season]
        
        # Day of year for seasonal variation, e.g. December 1st is day 365
        day_of_year = date.timetuple().tm_yday
        
        # We calculate 2*np.pi * (day_of_year - 15) / 365, which gives us an angle in radians.
        # (day_of_year - 15) gives us the day offset from January 15.
        # Dividing by 365 normalizes the day number to a fraction (0 to 1), so that when we multiply
        # by 2*np.pi (≈ 6.28, one full circle), we get exactly one complete cycle (0 to 2π radians)
        # over the entire year. Without dividing by 365, we'd get many cycles instead of one.
        # The angle ranges from -0.25 to 6.02 because subtracting 15 shifts the range.
        # We pass this angle to np.sin(), which converts it to a value between -1 and +1.
        # This value (-1 = coldest, +1 = warmest) becomes our seasonal_factor, which we then
        # use to adjust the base temperature up or down. The "-15" shifts the entire sine wave
        # pattern by 15 days, making January 15 the zero point.
        seasonal_factor = np.sin(2 * np.pi * (day_of_year - 15) / 365)
        base_temp = climate['avg_temp'] + 7 * seasonal_factor
        
        # Add daily variation
        # temp_variation is a random offset from normal distribution (mean=0, std=3)
        # Most values are between -3 and +3°C, but can range roughly from -9 to +9°C
        # temp_max adds a 2-6°C gap above, temp_min subtracts a 2-6°C gap below
        temp_variation = np.random.normal(0, 3)
        temp_max = base_temp + temp_variation + np.random.uniform(2, 6)
        temp_min = base_temp + temp_variation - np.random.uniform(2, 6)
        
        # Fix edge case: if random variations cause min >= max, set min to max minus 3-8°C gap
        if temp_min >= temp_max:
            temp_min = temp_max - np.random.uniform(3, 8)
        
        # Clamp to realistic ranges for configured city
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
    parser = argparse.ArgumentParser(description='Generate weather dataset for configured city')
    parser.parse_args()
    generate_weather()


if __name__ == '__main__':
    main()
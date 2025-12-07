import pandas as pd
import os
import config
from functools import lru_cache
from data_cleaning import clean_dataset

@lru_cache(maxsize=1)
def load_raw_data():
    """Load raw data from CSV files. Cached."""
    bookings_path = os.path.join(config.DATASETS_PATH, 'bookings.csv')
    events_path = os.path.join(config.DATASETS_PATH, 'events.csv')
    weather_path = os.path.join(config.DATASETS_PATH, 'weather.csv')
    web_analytics_path = os.path.join(config.DATASETS_PATH, 'web_analytics.csv')
    
    bookings = pd.read_csv(bookings_path) if os.path.exists(bookings_path) else pd.DataFrame()
    events = pd.read_csv(events_path) if os.path.exists(events_path) else pd.DataFrame()
    weather = pd.read_csv(weather_path) if os.path.exists(weather_path) else pd.DataFrame()
    web_analytics = pd.read_csv(web_analytics_path) if os.path.exists(web_analytics_path) else pd.DataFrame()
    
    return bookings, events, weather, web_analytics

@lru_cache(maxsize=1)
def get_data():
    """Load and clean all datasets. Uses cached raw data, caches cleaned result."""
    bookings_raw, events_raw, weather_raw, web_analytics_raw = load_raw_data()
    
    bookings, _ = clean_dataset(bookings_raw, 'bookings')
    events, _ = clean_dataset(events_raw, 'events')
    weather, _ = clean_dataset(weather_raw, 'weather')
    web_analytics, _ = clean_dataset(web_analytics_raw, 'web_analytics')
    
    return bookings, events, weather, web_analytics

def get_raw_data():
    """Get raw (uncleaned) datasets from cache."""
    return load_raw_data()
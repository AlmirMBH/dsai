import pandas as pd
import os
import config
from functools import lru_cache
from data_cleaning import clean_dataset

@lru_cache(maxsize=1)
def load_raw_data():
    """Load raw data from CSV files. Cached."""
    bookings = pd.read_csv(config.BOOKINGS_FILE) if os.path.exists(config.BOOKINGS_FILE) else pd.DataFrame()
    events = pd.read_csv(config.EVENTS_FILE) if os.path.exists(config.EVENTS_FILE) else pd.DataFrame()
    weather = pd.read_csv(config.WEATHER_FILE) if os.path.exists(config.WEATHER_FILE) else pd.DataFrame()
    web_analytics = pd.read_csv(config.WEB_ANALYTICS_FILE) if os.path.exists(config.WEB_ANALYTICS_FILE) else pd.DataFrame()
    bus_schedules = pd.read_csv(config.BUS_SCHEDULES_FILE) if os.path.exists(config.BUS_SCHEDULES_FILE) else pd.DataFrame()
    
    return bookings, events, weather, web_analytics, bus_schedules

@lru_cache(maxsize=1)
def get_data():
    """Load and clean all datasets. Uses cached raw data, caches cleaned result."""
    bookings_raw, events_raw, weather_raw, web_analytics_raw, bus_schedules_raw = load_raw_data()
    
    bookings, _ = clean_dataset(bookings_raw, 'bookings')
    events, _ = clean_dataset(events_raw, 'events')
    weather, _ = clean_dataset(weather_raw, 'weather')
    web_analytics, _ = clean_dataset(web_analytics_raw, 'web_analytics')
    bus_schedules, _ = clean_dataset(bus_schedules_raw, 'bus_schedules')
    
    return bookings, events, weather, web_analytics, bus_schedules

def get_raw_data():
    """Get raw (uncleaned) datasets from cache."""
    return load_raw_data()
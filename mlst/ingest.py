import pandas as pd
import os
import config

def load_data():
    bookings_path = os.path.join(config.DATASETS_PATH, 'bookings.csv')
    events_path = os.path.join(config.DATASETS_PATH, 'events.csv')
    weather_path = os.path.join(config.DATASETS_PATH, 'weather.csv')
    
    bookings = pd.read_csv(bookings_path) if os.path.exists(bookings_path) else pd.DataFrame()
    events = pd.read_csv(events_path) if os.path.exists(events_path) else pd.DataFrame()
    weather = pd.read_csv(weather_path) if os.path.exists(weather_path) else pd.DataFrame()
    
    return bookings, events, weather


import pandas as pd
import config

def load_data():
    bookings = pd.read_csv(config.BOOKINGS_FILE)
    events = pd.read_csv(config.EVENTS_FILE)
    weather = pd.read_csv(config.WEATHER_FILE)
    return bookings, events, weather


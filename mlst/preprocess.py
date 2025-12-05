import pandas as pd

def preprocess(bookings, events, weather):
    bookings['date'] = pd.to_datetime(bookings['date'])
    events['date'] = pd.to_datetime(events['date'])
    weather['date'] = pd.to_datetime(weather['date'])
    
    daily = bookings.groupby('date').agg({
        'rooms_booked': 'sum',
        'revenue_available_room': 'sum',
        'accommodation_units': 'sum'
    }).reset_index()
    
    daily['revpar'] = daily['revenue_available_room'] / daily['accommodation_units']
    daily['demand'] = daily['rooms_booked']
    
    event_intensity = events.groupby('date')['expected_attendance'].sum().reset_index()
    event_intensity.columns = ['date', 'event_intensity']
    
    weather['rain_flag'] = (weather['precipitation'] > 0).astype(int)
    
    df = daily.merge(event_intensity, on='date', how='left')
    df = df.merge(weather[['date', 'rain_flag', 'temperature_max']], on='date', how='left')
    
    df['event_intensity'] = df['event_intensity'].fillna(0)
    df['rain_flag'] = df['rain_flag'].fillna(0)
    df['temperature_max'] = df['temperature_max'].fillna(df['temperature_max'].mean())
    
    df['month'] = df['date'].dt.month
    
    return df


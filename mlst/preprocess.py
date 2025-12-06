import pandas as pd

def preprocess(bookings, events, weather):
    bookings['date'] = pd.to_datetime(bookings['date'])
    bookings['arrival_date'] = pd.to_datetime(bookings['arrival_date'])
    bookings['departure_date'] = pd.to_datetime(bookings['departure_date'])
    events['date'] = pd.to_datetime(events['date'])
    weather['date'] = pd.to_datetime(weather['date'])
    
    bookings['stay_nights'] = (bookings['departure_date'] - bookings['arrival_date']).dt.days
    bookings['total_revenue'] = bookings['average_daily_rate'] * bookings['stay_nights']
    
    daily = bookings.groupby('date').agg({
        'rooms_booked': 'sum',
        'total_revenue': 'sum',
        'accommodation_units': 'sum'
    }).reset_index()
    
    daily['revpar'] = daily['total_revenue'] / daily['accommodation_units']
    daily['demand'] = daily['rooms_booked']
    
    event_intensity = events.groupby('date')['expected_attendance'].sum().reset_index()
    event_intensity.columns = ['date', 'event_intensity']
    
    weather['rain_flag'] = (weather['precipitation'] > 0).astype(int)
    
    df = daily.merge(event_intensity, on='date', how='left')
    df = df.merge(weather[['date', 'rain_flag', 'temperature_max']], on='date', how='left')
    
    df['event_intensity'] = df['event_intensity'].fillna(0)
    df['rain_flag'] = df['rain_flag'].fillna(0)
    df['temperature_max'] = df.groupby(df['date'].dt.month)['temperature_max'].transform(lambda x: x.fillna(x.mean()))
    
    df['month'] = df['date'].dt.month
    
    return df


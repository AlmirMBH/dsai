import pandas as pd

def preprocess(bookings, events, weather, bus_schedules):
    bookings['date'] = pd.to_datetime(bookings['date'])
    bookings['arrival_date'] = pd.to_datetime(bookings['arrival_date'])
    bookings['departure_date'] = pd.to_datetime(bookings['departure_date'])
    events['date'] = pd.to_datetime(events['date'])
    weather['date'] = pd.to_datetime(weather['date'])
    bus_schedules['date'] = pd.to_datetime(bus_schedules['date'])
    
    bookings['stay_nights'] = (bookings['departure_date'] - bookings['arrival_date']).dt.days
    bookings['total_revenue'] = bookings['average_daily_rate'] * bookings['stay_nights']
    
    daily = bookings.groupby('date').agg({
        'rooms_booked': 'sum',
        'total_revenue': 'sum'
    }).reset_index()
    
    total_available_units = bookings['accommodation_units'].drop_duplicates().sum()
    
    # Fill gaps in the time series with 0
    all_dates = pd.date_range(start=daily['date'].min(), end=daily['date'].max(), freq='D')
    daily = daily.set_index('date').reindex(all_dates, fill_value=0).reset_index()
    daily.rename(columns={'index': 'date'}, inplace=True)
    daily['revpar'] = daily['total_revenue'] / total_available_units
    daily['demand'] = daily['rooms_booked']
    
    event_intensity = events.groupby('date')['expected_attendance'].sum().reset_index()
    event_intensity.columns = ['date', 'event_intensity']
    
    weather['rain_flag'] = (weather['precipitation'] > 0).astype(int)
    
    if not bus_schedules.empty:
        first_stops = bus_schedules.groupby('route_id')['stop_id'].first().to_dict()
        bus_first_stops = bus_schedules[
            bus_schedules.apply(lambda row: row['stop_id'] == first_stops.get(row['route_id']), axis=1)
        ]
        bus_trips = bus_first_stops.groupby('date').size().reset_index()
        bus_trips.columns = ['date', 'bus_trip_count']
    else:
        bus_trips = pd.DataFrame(columns=['date', 'bus_trip_count'])

    df = daily.merge(event_intensity, on='date', how='left')
    df = df.merge(weather[['date', 'rain_flag', 'temperature_max']], on='date', how='left')
    df = df.merge(bus_trips, on='date', how='left')
    df['temperature_max'] = df['temperature_max'] / 10.0
    
    df['event_intensity'] = df['event_intensity'].fillna(0)
    df['rain_flag'] = df['rain_flag'].fillna(0)
    df['bus_trip_count'] = df['bus_trip_count'].fillna(0)
    
    # Fill missing temperature_max with monthly mean
    monthly_means = df.groupby(df['date'].dt.month)['temperature_max'].mean()
    df['temperature_max'] = df['temperature_max'].fillna(df['date'].dt.month.map(monthly_means))
    
    df['month'] = df['date'].dt.month
    
    return df
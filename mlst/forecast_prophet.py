from prophet import Prophet
import pandas as pd
import config
from data_ingestion import get_data

def train_forecast(df, target='demand', periods=config.DEFAULT_FORECAST_PERIODS):
    df_prophet = df[['date', target, 'event_intensity', 'rain_flag', 'temperature_max', 'bus_trip_count']].copy()
    df_prophet.columns = ['ds', 'y', 'event_intensity', 'rain_flag', 'temperature_max', 'bus_trip_count']
    
    model = Prophet()
    model.add_regressor('event_intensity')
    model.add_regressor('rain_flag')
    model.add_regressor('temperature_max')
    model.add_regressor('bus_trip_count')
    model.fit(df_prophet)
    
    future = model.make_future_dataframe(periods=periods)
    future = future.merge(df_prophet[['ds', 'event_intensity', 'rain_flag', 'temperature_max', 'bus_trip_count']], on='ds', how='left')
    
    last_historical_date = df_prophet['ds'].max()
    future_dates_mask = future['ds'] > last_historical_date
    
    if future_dates_mask.any():
        _, events, weather, _, bus_schedules = get_data()
        events['date'] = pd.to_datetime(events['date'])
        weather['date'] = pd.to_datetime(weather['date'])
        bus_schedules['date'] = pd.to_datetime(bus_schedules['date'])
        
        future_dates = future[future_dates_mask]['ds']
        future_events = events[events['date'].isin(future_dates)]
        future_weather = weather[weather['date'].isin(future_dates)]
        future_bus = bus_schedules[bus_schedules['date'].isin(future_dates)]
        
        if len(future_events) > 0:
            event_intensity = future_events.groupby('date')['expected_attendance'].sum().reset_index()
            event_intensity.columns = ['ds', 'event_intensity_new']
            future = future.merge(event_intensity, on='ds', how='left')
            future['event_intensity'] = future['event_intensity'].fillna(future['event_intensity_new'])
            future = future.drop(columns=['event_intensity_new'])
        
        if len(future_weather) > 0:
            future_weather['rain_flag'] = (future_weather['precipitation'] > 0).astype(int)
            weather_future = future_weather[['date', 'rain_flag', 'temperature_max']].copy()
            weather_future.columns = ['ds', 'rain_flag_new', 'temperature_max_new']
            future = future.merge(weather_future, on='ds', how='left')
            future['rain_flag'] = future['rain_flag'].fillna(future['rain_flag_new'])
            future['temperature_max'] = future['temperature_max'].fillna(future['temperature_max_new'])
            future = future.drop(columns=['rain_flag_new', 'temperature_max_new'])

        if len(future_bus) > 0:
            bus_counts = future_bus.groupby('date').agg({'route_id': 'count'}).reset_index()
            bus_counts.columns = ['ds', 'bus_trip_count_new']
            future = future.merge(bus_counts, on='ds', how='left')
            future['bus_trip_count'] = future['bus_trip_count'].fillna(future['bus_trip_count_new'])
            future = future.drop(columns=['bus_trip_count_new'])
    
    future['month'] = future['ds'].dt.month
    historical_monthly_temperature = df_prophet.groupby(df_prophet['ds'].dt.month)['temperature_max'].mean()
    historical_monthly_event_intensity = df_prophet.groupby(df_prophet['ds'].dt.month)['event_intensity'].mean()
    historical_monthly_rain_flag = df_prophet.groupby(df_prophet['ds'].dt.month)['rain_flag'].median()
    historical_monthly_bus_trips = df_prophet.groupby(df_prophet['ds'].dt.month)['bus_trip_count'].mean()

    future['temperature_max'] = future['temperature_max'].fillna(future['month'].map(historical_monthly_temperature))
    future['event_intensity'] = future['event_intensity'].fillna(future['month'].map(historical_monthly_event_intensity))
    future['rain_flag'] = future['rain_flag'].fillna(future['month'].map(historical_monthly_rain_flag))
    future['bus_trip_count'] = future['bus_trip_count'].fillna(future['month'].map(historical_monthly_bus_trips))

    future['temperature_max'] = future['temperature_max'].fillna(df_prophet['temperature_max'].mean())
    future['event_intensity'] = future['event_intensity'].fillna(0)
    future['rain_flag'] = future['rain_flag'].fillna(0)
    future['bus_trip_count'] = future['bus_trip_count'].fillna(df_prophet['bus_trip_count'].mean())
    
    future = future.drop(columns=['month'])
    
    forecast = model.predict(future)
    return model, forecast

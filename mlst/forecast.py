from prophet import Prophet
import pandas as pd
import config
from data_ingestion import get_data

def train_forecast(df, target='demand', periods=config.DEFAULT_FORECAST_PERIODS):
    df_prophet = df[['date', target, 'event_intensity', 'rain_flag', 'temperature_max']].copy()
    df_prophet.columns = ['ds', 'y', 'event_intensity', 'rain_flag', 'temperature_max']
    
    model = Prophet()
    model.add_regressor('event_intensity')
    model.add_regressor('rain_flag')
    model.add_regressor('temperature_max')
    model.fit(df_prophet)
    
    future = model.make_future_dataframe(periods=periods)
    future = future.merge(df_prophet[['ds', 'event_intensity', 'rain_flag', 'temperature_max']], on='ds', how='left')
    
    last_historical_date = df_prophet['ds'].max()
    future_dates_mask = future['ds'] > last_historical_date
    
    if future_dates_mask.any():
        _, events, weather, _ = get_data()
        events['date'] = pd.to_datetime(events['date'])
        weather['date'] = pd.to_datetime(weather['date'])
        
        future_dates = future[future_dates_mask]['ds']
        future_events = events[events['date'].isin(future_dates)]
        future_weather = weather[weather['date'].isin(future_dates)]
        
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
    
    # TODO: Handle NaNs in a better way at a later stage (in the preprocess.py file)
    # TODO: Improve default values (0, 0, mean) - consider using forecasts or better heuristics
    future['event_intensity'] = future['event_intensity'].fillna(0)
    future['rain_flag'] = future['rain_flag'].fillna(0)
    future['temperature_max'] = future['temperature_max'].fillna(df_prophet['temperature_max'].mean())
    
    forecast = model.predict(future)
    return model, forecast
from prophet import Prophet
import pandas as pd
import config

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
    future['event_intensity'] = future['event_intensity'].fillna(0)
    future['rain_flag'] = future['rain_flag'].fillna(0)
    future['temperature_max'] = future['temperature_max'].fillna(df_prophet['temperature_max'].mean())
    
    forecast = model.predict(future)
    return model, forecast


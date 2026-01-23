import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from forecast import train_forecast
from data_ingestion import get_data
from dataset_aggregation_by_day import preprocess
import config

def render_forecast():
    bookings, events, weather, _, bus_schedules = get_data()
    if len(bookings) == 0 or len(events) == 0:
        st.write("No datasets available. Please generate datasets first.")
        return
    
    df = preprocess(bookings, events, weather, bus_schedules)
    st.header("Demand & RevPAR Forecast")
    periods = st.slider("Forecast periods", 7, 90, config.DEFAULT_FORECAST_PERIODS)
    
    today = pd.Timestamp(date.today())
    df_historical = df[df['date'] <= today].copy()
    
    _, forecast_demand = train_forecast(df_historical, target='demand', periods=periods)
    _, forecast_revpar = train_forecast(df_historical, target='revpar', periods=periods)
    
    forecast_demand_future = forecast_demand[forecast_demand['ds'] > today].head(periods)
    forecast_revpar_future = forecast_revpar[forecast_revpar['ds'] > today].head(periods)
    
    if len(forecast_demand_future) > 0:
        forecast_end = forecast_demand_future['ds'].max()
        xlim_start = max(today - pd.Timedelta(days=30), df_historical['date'].min())
        xlim_end = forecast_end
    else:
        xlim_start = df_historical['date'].min()
        xlim_end = today
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    ax1.plot(df_historical['date'], df_historical['demand'], label='Actual')
    ax1.plot(forecast_demand_future['ds'], forecast_demand_future['yhat'], label='Forecast')
    ax1.set_title('Demand Forecast')
    ax1.set_xlim(xlim_start, xlim_end)
    ax1.legend()
    
    ax2.plot(df_historical['date'], df_historical['revpar'], label='Actual', color='green')
    ax2.plot(forecast_revpar_future['ds'], forecast_revpar_future['yhat'], label='Forecast', color='brown')
    ax2.set_title('RevPAR Forecast')
    ax2.set_xlim(xlim_start, xlim_end)
    ax2.legend()
    
    st.pyplot(fig)
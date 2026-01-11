import streamlit as st
import matplotlib.pyplot as plt
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
    
    _, forecast_demand = train_forecast(df, target='demand', periods=periods)
    _, forecast_revpar = train_forecast(df, target='revpar', periods=periods)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    ax1.plot(df['date'], df['demand'], label='Actual')
    ax1.plot(forecast_demand['ds'], forecast_demand['yhat'], label='Forecast')
    ax1.set_title('Demand Forecast')
    ax1.legend()
    
    ax2.plot(df['date'], df['revpar'], label='Actual')
    ax2.plot(forecast_revpar['ds'], forecast_revpar['yhat'], label='Forecast')
    ax2.set_title('RevPAR Forecast')
    ax2.legend()
    
    st.pyplot(fig)
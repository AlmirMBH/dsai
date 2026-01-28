import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from forecast_prophet import train_forecast
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
    periods = st.slider("Forecast periods", 7, 90, config.DEFAULT_FORECAST_PERIODS, key="prophet_forecast_periods")
    
    today = pd.Timestamp(date.today())
    df_historical = df[df['date'] <= today].copy()
    
    _, forecast_demand = train_forecast(df_historical, target='demand', periods=periods)
    _, forecast_revpar = train_forecast(df_historical, target='revpar', periods=periods)
    
    forecast_demand_future = forecast_demand[forecast_demand['ds'] > today].head(periods)
    forecast_revpar_future = forecast_revpar[forecast_revpar['ds'] > today].head(periods)

    if len(forecast_demand_future) > 0:
        forecast_start = forecast_demand_future['ds'].min()
        forecast_end = forecast_demand_future['ds'].max()
        last_year_start = forecast_start - pd.DateOffset(years=1)
        last_year_end = forecast_end - pd.DateOffset(years=1)
        df_last_year = df_historical[(df_historical['date'] >= last_year_start) & (df_historical['date'] <= last_year_end)]

        st.subheader("RevPAR")
        fig_r, (ax_r_fc, ax_r_ly) = plt.subplots(1, 2, figsize=(12, 4))
        ax_r_fc.plot(forecast_revpar_future['ds'], forecast_revpar_future['yhat'])
        ax_r_fc.set_title("Forecast (forecast period only)")
        ax_r_fc.set_xlim(forecast_start, forecast_end)
        ax_r_ly.set_title("Actual (same period last year)")
        ax_r_ly.set_xlim(last_year_start, last_year_end)
        if len(df_last_year) > 0:
            ax_r_ly.plot(df_last_year['date'], df_last_year['revpar'])
        fig_r.autofmt_xdate()
        st.pyplot(fig_r)
        plt.close(fig_r)

        st.subheader("Demand")
        fig_d, (ax_d_fc, ax_d_ly) = plt.subplots(1, 2, figsize=(12, 4))
        ax_d_fc.plot(forecast_demand_future['ds'], forecast_demand_future['yhat'])
        ax_d_fc.set_title("Forecast (forecast period only)")
        ax_d_fc.set_xlim(forecast_start, forecast_end)
        ax_d_ly.set_title("Actual (same period last year)")
        ax_d_ly.set_xlim(last_year_start, last_year_end)
        if len(df_last_year) > 0:
            ax_d_ly.plot(df_last_year['date'], df_last_year['demand'])
        fig_d.autofmt_xdate()
        st.pyplot(fig_d)
        plt.close(fig_d)
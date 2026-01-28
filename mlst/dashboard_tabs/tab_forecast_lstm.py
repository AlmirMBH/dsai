import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from data_ingestion import get_data
from dataset_aggregation_by_day import preprocess
from lstm_forecast import train_forecast_lstm, predict_forecast_lstm
import config

LSTM_CACHE_KEY = "lstm_models"
TIME_STEPS = 5

def render_forecast_lstm():
    bookings, events, weather, _, bus_schedules = get_data()
    if len(bookings) == 0 or len(events) == 0:
        st.warning("No datasets available. Generate datasets first.")
        return
    df = preprocess(bookings, events, weather, bus_schedules)
    st.header("Demand & RevPAR Forecast")
    if st.button("Re-run model", key="lstm_rerun"):
        if LSTM_CACHE_KEY in st.session_state:
            del st.session_state[LSTM_CACHE_KEY]
        st.rerun()
    periods = st.slider("Forecast periods", 7, 90, config.DEFAULT_FORECAST_PERIODS, key="lstm_forecast_periods")
    today = pd.Timestamp(date.today())
    df_historical = df[df["date"] <= today].copy()
    if len(df_historical) < TIME_STEPS + 2:
        st.warning("Not enough historical data. Need at least {} days.".format(TIME_STEPS + 2))
        return
    if LSTM_CACHE_KEY in st.session_state:
        cached = st.session_state[LSTM_CACHE_KEY]
        forecast_dates_d, forecast_demand, forecast_dates_r, forecast_revpar = predict_forecast_lstm(
            cached[0], cached[1], cached[2], cached[3], df_historical, periods, time_steps=TIME_STEPS
        )
    else:
        with st.spinner("Training LSTM…"):
            models_scalers, forecast_dates_d, forecast_demand, forecast_dates_r, forecast_revpar = train_forecast_lstm(
                df_historical, periods, time_steps=TIME_STEPS
            )
            st.session_state[LSTM_CACHE_KEY] = models_scalers
    forecast_demand_future = pd.DataFrame({"ds": forecast_dates_d, "yhat": forecast_demand})
    forecast_revpar_future = pd.DataFrame({"ds": forecast_dates_r, "yhat": forecast_revpar})
    if len(forecast_demand_future) > 0:
        forecast_start = forecast_demand_future["ds"].min()
        forecast_end = forecast_demand_future["ds"].max()
        last_year_start = forecast_start - pd.DateOffset(years=1)
        last_year_end = forecast_end - pd.DateOffset(years=1)
        df_last_year = df_historical[
            (df_historical["date"] >= last_year_start) & (df_historical["date"] <= last_year_end)
        ]
        st.subheader("RevPAR")
        fig_r, (ax_r_fc, ax_r_ly) = plt.subplots(1, 2, figsize=(12, 4))
        ax_r_fc.plot(forecast_revpar_future["ds"], forecast_revpar_future["yhat"])
        ax_r_fc.set_title("Forecast (forecast period only)")
        ax_r_fc.set_xlim(forecast_start, forecast_end)
        ax_r_ly.set_title("Actual (same period last year)")
        ax_r_ly.set_xlim(last_year_start, last_year_end)
        if len(df_last_year) > 0:
            ax_r_ly.plot(df_last_year["date"], df_last_year["revpar"])
        fig_r.autofmt_xdate()
        st.pyplot(fig_r)
        plt.close(fig_r)
        st.subheader("Demand")
        fig_d, (ax_d_fc, ax_d_ly) = plt.subplots(1, 2, figsize=(12, 4))
        ax_d_fc.plot(forecast_demand_future["ds"], forecast_demand_future["yhat"])
        ax_d_fc.set_title("Forecast (forecast period only)")
        ax_d_fc.set_xlim(forecast_start, forecast_end)
        ax_d_ly.set_title("Actual (same period last year)")
        ax_d_ly.set_xlim(last_year_start, last_year_end)
        if len(df_last_year) > 0:
            ax_d_ly.plot(df_last_year["date"], df_last_year["demand"])
        fig_d.autofmt_xdate()
        st.pyplot(fig_d)
        plt.close(fig_d)

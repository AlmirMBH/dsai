import streamlit as st
from ingest import load_data
from preprocess import preprocess
from forecast import train_forecast
from personas import create_personas
from recommend import recommend_events
from impact import measure_impact
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
import config

st.title("Tourism Forecasting & Recommendations")

bookings, events, weather = load_data()
if len(bookings) == 0 or len(events) == 0:
    st.write("No datasets available. Please generate datasets first.")
    st.stop()

df = preprocess(bookings, events, weather)
personas = create_personas(bookings)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["EDA", "Forecast", "Impact", "Recommendations", "Itinerary"])

with tab1:
    st.header("Exploratory Data Analysis")
    
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    df.sort_values('date').set_index('date')['demand'].plot(ax=ax1)
    ax1.set_title('Rooms Sold Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Rooms Sold')
    st.pyplot(fig1)
    
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    df.groupby(df['date'].dt.month)['demand'].mean().plot(kind='bar', ax=ax2)
    ax2.set_title('Average Rooms Sold by Month')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Avg Rooms Sold')
    st.pyplot(fig2)
    
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    df['revpar'].dropna().hist(bins=40, ax=ax3)
    ax3.set_title('RevPAR Distribution')
    ax3.set_xlabel('RevPAR')
    ax3.set_ylabel('Frequency')
    st.pyplot(fig3)
    
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    df.plot.scatter(x='temperature_max', y='demand', ax=ax4)
    ax4.set_title('Rooms Sold vs Temperature')
    st.pyplot(fig4)
    
    fig5, ax5 = plt.subplots(figsize=(10, 4))
    df.boxplot(column='demand', by='event_intensity', ax=ax5)
    ax5.set_title('Rooms Sold by Event Intensity')
    st.pyplot(fig5)

with tab2:
    st.header("Demand & RevPAR Forecast")
    periods = st.slider("Forecast periods", 7, 90, config.DEFAULT_FORECAST_PERIODS)
    
    model_demand, forecast_demand = train_forecast(df, target='demand', periods=periods)
    model_revpar, forecast_revpar = train_forecast(df, target='revpar', periods=periods)
    
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

with tab3:
    st.header("Impact Measurement")
    sample_recs = recommend_events(1, config.DEFAULT_RECOMMENDATIONS * 2)
    impact = measure_impact(bookings, sample_recs)
    
    st.metric("Conversion Rate", f"{impact['conversion_rate']:.2%}")
    st.metric("Avg Bookings (with recs)", f"{impact['avg_bookings_with_recommendations']:.2f}")
    st.metric("Avg Bookings (without recs)", f"{impact['avg_bookings_without_recommendations']:.2f}")
    st.metric("Improvement", f"{impact['improvement']:.2f}%")

with tab4:
    st.header("Event Recommendations")
    guest_id = st.number_input("Guest ID", min_value=1, value=1)
    n = st.slider("Number of recommendations", 1, 20, config.DEFAULT_RECOMMENDATIONS)
    
    today = date.today()
    default_end = today + timedelta(days=config.DEFAULT_RECOMMENDATION_DAYS)
    start_date = st.date_input("Start date", value=today, min_value=today)
    end_date = st.date_input("End date", value=default_end, min_value=today)
    
    if start_date and end_date:
        recs = recommend_events(guest_id, n, start_date, end_date)
    else:
        recs = pd.DataFrame()
    
    if len(recs) > 0:
        st.dataframe(recs[['date', 'type', 'name', 'location', 'expected_attendance']].reset_index(drop=True))
    else:
        st.write("No available events")

with tab5:
    st.header("Itinerary")
    guest_id = st.number_input("Guest ID", min_value=1, value=1, key="itinerary_guest")
    days = st.slider("Number of days", 1, 10, config.DEFAULT_ITINERARY_DAYS)
    n_per_day = st.slider("Events per day", 1, 5, config.DEFAULT_EVENTS_PER_DAY)
    
    today = date.today()
    default_end = today + timedelta(days=config.DEFAULT_RECOMMENDATION_DAYS)
    start_date = st.date_input("Start date", value=today, min_value=today, key="itinerary_start")
    end_date = st.date_input("End date", value=default_end, min_value=today, key="itinerary_end")
    
    if start_date and end_date:
        recs = recommend_events(guest_id, n=days * n_per_day, start_date=start_date, end_date=end_date)
    else:
        recs = pd.DataFrame()
    
    if len(recs) > 0:
        st.dataframe(recs[['date', 'type', 'name', 'location', 'expected_attendance']].reset_index(drop=True))
    else:
        st.write("No available events")
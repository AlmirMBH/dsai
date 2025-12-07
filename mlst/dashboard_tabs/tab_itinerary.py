import streamlit as st
import pandas as pd
from datetime import date, timedelta
from recommend import recommend_events
import config

def render_itinerary():
    """Render Itinerary tab."""
    st.header("Itinerary")
    guest_id = st.number_input("Guest ID", min_value=1, value=1, key="itinerary_guest")
    n_per_day = st.slider("Events per day", 1, 5, config.DEFAULT_EVENTS_PER_DAY)
    
    today = date.today()
    default_end = today + timedelta(days=config.DEFAULT_RECOMMENDATION_DAYS)
    start_date = st.date_input("Start date", value=today, min_value=today, key="itinerary_start")
    end_date = st.date_input("End date", value=default_end, min_value=today, key="itinerary_end")
    
    if start_date and end_date:
        actual_days = (end_date - start_date).days + 1
        recs = recommend_events(guest_id, n=actual_days * n_per_day, start_date=start_date, end_date=end_date)
    else:
        recs = pd.DataFrame()
    
    if len(recs) > 0:
        recs['date_only'] = pd.to_datetime(recs['date']).dt.date
        recs_grouped = recs.groupby('date_only').head(n_per_day)
        st.dataframe(recs_grouped[['date', 'time', 'type', 'name', 'location', 'expected_attendance']].reset_index(drop=True))
    else:
        st.write("No available events")
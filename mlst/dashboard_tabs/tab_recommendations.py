import streamlit as st
import pandas as pd
from datetime import date, timedelta
from recommend import recommend_events
import config

def render_recommendations():
    """Render Recommendations tab."""
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
        st.dataframe(recs[['date', 'time', 'type', 'name', 'location', 'expected_attendance']].reset_index(drop=True))
    else:
        st.write("No available events")
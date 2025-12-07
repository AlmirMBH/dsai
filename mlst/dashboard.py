import streamlit as st
from dashboard_tabs.tab_data_processing import render_data_processing
from dashboard_tabs.tab_eda import render_eda
from dashboard_tabs.tab_forecast import render_forecast
from dashboard_tabs.tab_impact import render_impact
from dashboard_tabs.tab_recommendations import render_recommendations
from dashboard_tabs.tab_itinerary import render_itinerary

st.title("Tourism Forecasting & Recommendations")

tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Processing", "EDA", "Forecast", "Impact", "Recommendations", "Itinerary"])

with tab0:
    render_data_processing()

with tab1:
    render_eda()

with tab2:
    render_forecast()

with tab3:
    render_impact()

with tab4:
    render_recommendations()

with tab5:
    render_itinerary()
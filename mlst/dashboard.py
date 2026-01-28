import streamlit as st

import tensorflow as tf
tf.constant(1)

from dashboard_tabs.tab_data_processing import render_data_processing
from dashboard_tabs.tab_eda import render_eda
from dashboard_tabs.tab_forecast import render_forecast
from dashboard_tabs.tab_impact import render_impact
from dashboard_tabs.tab_recommendations import render_recommendations
from dashboard_tabs.tab_itinerary import render_itinerary

st.title("Tourism Forecasting & Recommendations")

tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Data Processing", "EDA", "Forecast Prophet", "Impact", "Recommendations", "Itinerary", "Forecast LSTM"])

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

with tab6:
    from dashboard_tabs.tab_forecast_lstm import render_forecast_lstm
    render_forecast_lstm()
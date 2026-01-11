import streamlit as st
import pandas as pd
from impact import measure_impact
from data_ingestion import get_data

def render_impact():
    bookings, _, _, web_analytics, _ = get_data()
    if len(bookings) == 0:
        st.write("No datasets available. Please generate datasets first.")
        return
    
    st.header("Impact Measurement")
    impact = measure_impact(bookings, web_analytics)
    
    conversion_table = pd.DataFrame({'Metric': ['Conversion Rate'], 'Value': [f"{impact['conversion_rate']:.2%}"]})
    st.table(conversion_table)
    
    st.subheader("A/B Test Comparison")
    ab_metrics = ['Avg Bookings (Treatment)', 'Avg Bookings (Control)', 'Improvement']
    ab_values = [
        f"{impact['ab_test']['avg_treatment']:.4f}",
        f"{impact['ab_test']['avg_control']:.4f}",
        f"{impact['ab_test']['improvement']:.4f}%"
    ]
    ab_table = pd.DataFrame({'Metric': ab_metrics, 'Value': ab_values})
    st.table(ab_table)
    
    st.subheader("Difference-in-Differences")
    did_table = pd.DataFrame({'Metric': ['Causal Impact'], 'Value': [f"{impact['did']['improvement']:.4f}%"]})
    st.table(did_table)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_before_after_comparison(original_missing, final_missing, title="Data Completeness"):
    """Plot before/after missing data comparison."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Before Cleaning', 'After Cleaning'], [original_missing, final_missing])
    ax.set_title(title)
    ax.set_ylabel('Missing Values')
    return fig

def _get_bookings_cleaning_desc(meta):
    """Get cleaning description for bookings dataset."""
    desc = []
    if meta.get('invalid_values', 0) > 0:
        desc.append("fixed invalid dates where departure was less than or equal to arrival by setting departure to arrival plus one day")
    if meta.get('type_errors', 0) > 0:
        desc.append("converted type errors in the age column by removing 'years' suffix and parsing to numeric values")
    if meta.get('outliers', 0) > 0:
        desc.append("set outliers to missing values (age > 120 or < 0, negative prices)")
    desc.append("imputed missing numeric values using median for age, average_daily_rate, and revenue_available_room")
    desc.append("imputed missing categorical values with 'Unknown' for guest_country and email")
    desc.append("other columns (deleted_at, created_at, etc.) were not imputed")
    return desc

def _get_events_cleaning_desc(meta):
    """Get cleaning description for events dataset."""
    desc = []
    if meta.get('type_errors', 0) > 0:
        desc.append("fixed type errors in the name column by removing 'event' suffix")
    if meta.get('outliers', 0) > 0:
        desc.append("set outliers to missing values (negative attendance or attendance > 100000)")
    if meta.get('invalid_values', 0) > 0:
        desc.append("removed rows with invalid dates (before 2020-01-01)")
    desc.append("imputed missing text fields with 'Unknown' for name, location, and type")
    desc.append("imputed missing attendance values using median")
    return desc

def _get_weather_cleaning_desc(meta):
    """Get cleaning description for weather dataset."""
    desc = []
    if meta.get('type_errors', 0) > 0:
        desc.append("fixed type errors in temperature_max by removing 'C' suffix and parsing to numeric values")
    if meta.get('outliers', 0) > 0:
        desc.append("set negative precipitation to 0 and extreme temperature outliers (> 500°C or < -500°C) to missing values")
    if meta.get('invalid_values', 0) > 0:
        desc.append("removed rows with invalid dates (before 2020-01-01)")
    desc.append("imputed missing values using median for temperature_max, temperature_min, precipitation, and humidity")
    return desc

def _get_web_analytics_cleaning_desc(meta):
    """Get cleaning description for web analytics dataset."""
    desc = []
    if meta.get('type_errors', 0) > 0:
        desc.append("fixed invalid date format strings by replacing them with missing values")
    if meta.get('outliers', 0) > 0:
        desc.append("fixed invalid boolean values (values other than 0 or 1) by setting them to 0")
    if meta.get('invalid_values', 0) > 0 or meta.get('rows_dropped_missing_dates', 0) > 0:
        desc.append("dropped rows with missing or invalid dates (including dates before 2020-01-01)")
    return desc

def _get_cleaning_description(name, meta):
    """Get cleaning description for a dataset."""
    if meta.get('duplicates_removed', 0) > 0:
        base_desc = [f"removed {meta.get('duplicates_removed', 0)} duplicate rows"]
    else:
        base_desc = []
    
    desc_functions = {
        'Bookings': _get_bookings_cleaning_desc,
        'Events': _get_events_cleaning_desc,
        'Weather': _get_weather_cleaning_desc,
        'Web Analytics': _get_web_analytics_cleaning_desc
    }
    
    dataset_desc = desc_functions.get(name, lambda m: [])(meta)
    return base_desc + dataset_desc

def _format_cleaning_paragraph(name, cleaning_desc):
    """Format cleaning description as a paragraph."""
    if not cleaning_desc:
        return None
    if len(cleaning_desc) == 1:
        return f"For {name.lower()}, we {cleaning_desc[0]}."
    return f"For {name.lower()}, we " + ", ".join(cleaning_desc[:-1]) + f", and {cleaning_desc[-1]}."

def _create_raw_metrics_table(meta):
    """Create raw dataset metrics table."""
    original_rows = meta.get('original_shape', (0, 0))[0]
    rows_dropped = meta.get('rows_dropped', 0)
    drop_pct = (rows_dropped / original_rows * 100) if original_rows > 0 else 0
    
    metrics = ['Number of rows', 'Number of missing values', 'Number of duplicate rows', 
               'Type errors', 'Outliers', 'Invalid values', 'Rows dropped']
    values = [
        str(original_rows),
        str(meta.get('original_missing', 0)),
        str(meta.get('duplicates_removed', 0)),
        str(meta.get('type_errors', 0)),
        str(meta.get('outliers', 0)),
        str(meta.get('invalid_values', 0)),
        f"{rows_dropped} ({drop_pct:.2f}%)" if rows_dropped > 0 else "0"
    ]
    return pd.DataFrame({'Metric': metrics, 'Value': values})

def _create_cleaned_metrics_table(meta):
    """Create cleaned dataset metrics table."""
    metrics = ['Number of rows', 'Number of missing values', 'Percentage of correct values']
    values = [
        str(meta.get('final_shape', (0, 0))[0]),
        str(meta.get('final_missing', 0)),
        f"{meta.get('completeness', 0):.2%}"
    ]
    return pd.DataFrame({'Metric': metrics, 'Value': values})

def render_data_processing():
    """Render Data Processing tab."""
    from data_ingestion import get_data, get_raw_data
    from data_cleaning import clean_dataset
    
    bookings, events, weather, web_analytics = get_data()
    bookings_raw, events_raw, weather_raw, web_analytics_raw = get_raw_data()
    
    bookings_meta = {}
    events_meta = {}
    weather_meta = {}
    web_analytics_meta = {}
    
    if len(bookings_raw) > 0:
        _, bookings_meta = clean_dataset(bookings_raw, 'bookings')
    if len(events_raw) > 0:
        _, events_meta = clean_dataset(events_raw, 'events')
    if len(weather_raw) > 0:
        _, weather_meta = clean_dataset(weather_raw, 'weather')
    if len(web_analytics_raw) > 0:
        _, web_analytics_meta = clean_dataset(web_analytics_raw, 'web_analytics')
    
    st.header("Data Processing & Quality")
    
    datasets_info = [
        ("Bookings", bookings_raw, bookings, bookings_meta),
        ("Events", events_raw, events, events_meta),
        ("Weather", weather_raw, weather, weather_meta),
        ("Web Analytics", web_analytics_raw, web_analytics, web_analytics_meta)
    ]
    
    for name, raw_df, clean_df, meta in datasets_info:
        st.subheader(name)
        
        cleaning_desc = _get_cleaning_description(name, meta)
        paragraph = _format_cleaning_paragraph(name, cleaning_desc)
        if paragraph:
            st.write("**Cleaning operations performed:**")
            st.write(paragraph)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Raw Dataset**")
            st.table(_create_raw_metrics_table(meta))
        with col2:
            st.write("**Cleaned Dataset**")
            st.table(_create_cleaned_metrics_table(meta))
        
        if meta.get('original_missing', 0) > 0 or meta.get('final_missing', 0) > 0:
            fig = plot_before_after_comparison(
                meta.get('original_missing', 0),
                meta.get('final_missing', 0),
                f"{name} - Missing Cells"
            )
            st.pyplot(fig)
        
        st.divider()

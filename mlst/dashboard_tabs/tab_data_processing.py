import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import config

def plot_before_after_comparison(original_missing, final_missing, title="Data Completeness"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Before Cleaning', 'After Cleaning'], [original_missing, final_missing])
    ax.set_title(title)
    ax.set_ylabel('Missing Values')
    return fig

def _get_bookings_cleaning_description(metadata):
    description = []
    if metadata.get('invalid_values', 0) > 0:
        description.append("fixed invalid dates where departure was less than or equal to arrival by setting departure to arrival plus one day")
    if metadata.get('type_errors', 0) > 0:
        description.append("converted type errors in the age column by removing 'years' suffix and parsing to numeric values")
    if metadata.get('outliers', 0) > 0:
        description.append(f"set outliers to missing values (age > {config.GUEST_AGE_MAX} or < {config.GUEST_AGE_MIN}, negative prices)")
    description.append("imputed missing numeric values using median for age, average_daily_rate, and revenue_available_room")
    description.append("imputed missing categorical values with 'Unknown' for guest_country and email")
    description.append("other columns (deleted_at, created_at, etc.) were not imputed")
    return description

def _get_events_cleaning_description(metadata):
    description = []
    if metadata.get('type_errors', 0) > 0:
        description.append("fixed type errors in the name column by removing 'event' suffix")
    if metadata.get('outliers', 0) > 0:
        description.append(f"set outliers to missing values (negative attendance or attendance > {config.EVENT_ATTENDANCE_MAX})")
    if metadata.get('invalid_values', 0) > 0:
        description.append(f"removed rows with invalid dates (before {config.DATASET_START_DATE})")
    description.append("imputed missing text fields with 'Unknown' for name, location, and type")
    description.append("imputed missing attendance values using median")
    return description

def _get_weather_cleaning_description(metadata):
    description = []
    if metadata.get('type_errors', 0) > 0:
        description.append("fixed type errors in temperature_max by removing 'C' suffix and parsing to numeric values")
    if metadata.get('outliers', 0) > 0:
        description.append(f"set negative precipitation to 0 and extreme temperature outliers (> {config.TEMPERATURE_MAX_THRESHOLD/10}°C or < {config.TEMPERATURE_MIN_THRESHOLD/10}°C) to missing values")
    if metadata.get('invalid_values', 0) > 0:
        description.append(f"removed rows with invalid dates (before {config.DATASET_START_DATE})")
    description.append("imputed missing values using median for temperature_max, temperature_min, precipitation, and humidity")
    return description

def _get_web_analytics_cleaning_description(metadata):
    description = []
    if metadata.get('type_errors', 0) > 0:
        description.append("fixed invalid date format strings by replacing them with missing values")
    if metadata.get('outliers', 0) > 0:
        description.append("fixed invalid boolean values (values other than 0 or 1) by setting them to 0")
    if metadata.get('invalid_values', 0) > 0 or metadata.get('rows_dropped_missing_dates', 0) > 0:
        description.append(f"dropped rows with missing or invalid dates (including dates before {config.DATASET_START_DATE})")
    return description

def _get_bus_schedules_cleaning_description(metadata):
    description = []
    if metadata.get('invalid_values', 0) > 0:
        description.append(f"removed rows with invalid dates (before {config.DATASET_START_DATE})")
    description.append("imputed missing text fields with 'Unknown' for route_id, stop_id, and stop_name")
    return description

def _get_cleaning_description(name, metadata):
    if metadata.get('duplicates_removed', 0) > 0:
        base_description = [f"removed {metadata.get('duplicates_removed', 0)} duplicate rows"]
    else:
        base_description = []
    
    description_functions = {
        'Bookings': _get_bookings_cleaning_description,
        'Events': _get_events_cleaning_description,
        'Weather': _get_weather_cleaning_description,
        'Web Analytics': _get_web_analytics_cleaning_description,
        'Bus Schedules': _get_bus_schedules_cleaning_description
    }
    
    dataset_description = description_functions.get(name, lambda m: [])(metadata)
    return base_description + dataset_description

def _format_cleaning_paragraph(name, cleaning_description):
    if not cleaning_description:
        return None
    if len(cleaning_description) == 1:
        return f"For {name.lower()}, we {cleaning_description[0]}."
    return f"For {name.lower()}, we " + ", ".join(cleaning_description[:-1]) + f", and {cleaning_description[-1]}."

def _create_raw_metrics_table(metadata):
    original_rows = metadata.get('original_shape', (0, 0))[0]
    rows_dropped = metadata.get('rows_dropped', 0)
    drop_percentage = (rows_dropped / original_rows * 100) if original_rows > 0 else 0
    
    metrics = ['Number of rows', 'Number of missing values', 'Number of duplicate rows', 
               'Type errors', 'Outliers', 'Invalid values', 'Rows dropped']
    values = [
        str(original_rows),
        str(metadata.get('original_missing', 0)),
        str(metadata.get('duplicates_removed', 0)),
        str(metadata.get('type_errors', 0)),
        str(metadata.get('outliers', 0)),
        str(metadata.get('invalid_values', 0)),
        f"{rows_dropped} ({drop_percentage:.2f}%)" if rows_dropped > 0 else "0"
    ]
    return pd.DataFrame({'Metric': metrics, 'Value': values})

def _create_cleaned_metrics_table(metadata):
    metrics = ['Number of rows', 'Number of missing values', 'Percentage of correct values']
    values = [
        str(metadata.get('final_shape', (0, 0))[0]),
        str(metadata.get('final_missing', 0)),
        f"{metadata.get('completeness', 0):.2%}"
    ]
    return pd.DataFrame({'Metric': metrics, 'Value': values})

def render_data_processing():
    from data_ingestion import get_data, get_raw_data
    from data_cleaning import clean_dataset
    
    bookings, events, weather, web_analytics, bus_schedules = get_data()
    bookings_raw, events_raw, weather_raw, web_analytics_raw, bus_schedules_raw = get_raw_data()
    
    datasets_metadata = {}
    web_analytics_name = "Web Analytics"
    bus_schedules_name = "Bus Schedules"
    raw_datasets = {
        "Bookings": (bookings_raw, 'bookings'),
        "Events": (events_raw, 'events'),
        "Weather": (weather_raw, 'weather'),
        web_analytics_name: (web_analytics_raw, 'web_analytics'),
        bus_schedules_name: (bus_schedules_raw, 'bus_schedules')
    }
    
    for name, (dataframe, dataset_type) in raw_datasets.items():
        if len(dataframe) > 0:
            _, datasets_metadata[name] = clean_dataset(dataframe, dataset_type)
        else:
            datasets_metadata[name] = {}
    
    st.header("Data Processing & Quality")
    
    datasets_info = [
        ("Bookings", bookings_raw, bookings, datasets_metadata["Bookings"]),
        ("Events", events_raw, events, datasets_metadata["Events"]),
        ("Weather", weather_raw, weather, datasets_metadata["Weather"]),
        (web_analytics_name, web_analytics_raw, web_analytics, datasets_metadata[web_analytics_name]),
        (bus_schedules_name, bus_schedules_raw, bus_schedules, datasets_metadata[bus_schedules_name])
    ]
    
    for name, raw_dataframe, clean_dataframe, metadata in datasets_info:
        st.subheader(name)
        
        cleaning_description = _get_cleaning_description(name, metadata)
        paragraph = _format_cleaning_paragraph(name, cleaning_description)
        if paragraph:
            st.write("**Cleaning operations performed:**")
            st.write(paragraph)
        
        column1, column2 = st.columns(2)
        with column1:
            st.write("**Raw Dataset**")
            st.table(_create_raw_metrics_table(metadata))
        with column2:
            st.write("**Cleaned Dataset**")
            st.table(_create_cleaned_metrics_table(metadata))
        
        if metadata.get('original_missing', 0) > 0 or metadata.get('final_missing', 0) > 0:
            fig = plot_before_after_comparison(
                metadata.get('original_missing', 0),
                metadata.get('final_missing', 0),
                f"{name} - Missing Cells"
            )
            st.pyplot(fig)
        
        st.divider()

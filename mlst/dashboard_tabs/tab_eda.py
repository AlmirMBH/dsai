import streamlit as st
import matplotlib.pyplot as plt
from data_ingestion import get_data
from dataset_aggregation_by_day import preprocess

def render_eda():
    bookings, events, weather, _, bus_schedules = get_data()
    if len(bookings) == 0 or len(events) == 0:
        st.write("No datasets available. Please generate datasets first.")
        return
    
    df = preprocess(bookings, events, weather, bus_schedules)
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
    plt.suptitle('')
    ax5.set_title('Rooms Sold by Event Intensity')
    st.pyplot(fig5)

    st.subheader("Transport Analysis")
    fig6, ax6 = plt.subplots(figsize=(10, 4))
    df.plot.scatter(x='bus_trip_count', y='demand', ax=ax6)
    ax6.set_title('Rooms Sold vs Total Bus Arrivals')
    ax6.set_xlabel('Total Bus Arrivals')
    ax6.set_ylabel('Rooms Sold')
    st.pyplot(fig6)

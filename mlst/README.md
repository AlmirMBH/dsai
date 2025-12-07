# Tourism & Smart City Analytics

**Course:** Machine Learning: Supervised Techniques  
**Professor:** Amila Akagic  
**Authors:** Rijalda Sacirbegovic, Almir Mustafic, Benjamin Kljuno

## Overview

Tourism analytics system for Amsterdam that forecasts demand and RevPAR, and recommends events per persona.

## Objectives

- Forecast city/region demand and RevPAR
- Recommend itineraries/tours per persona
- Measure impact on bookings

## Datasets

Synthetic Amsterdam datasets (December 2023 to February 2026):
- bookings.csv - Accommodation bookings
- events.csv - Amsterdam events
- weather.csv - Daily weather data
- bus_schedules.csv - Bus schedules
- web_analytics.csv - Recommendation tracking data

Generate datasets:
```bash
python generate_all_datasets.py
```

### Dataset Generation

Datasets are generated in order: weather, events, bus schedules, bookings, web analytics, additional bookings.

**Events**: At least one event per day. Seasonal patterns (more in summer, weekends). Major annual events included.
- *Modeled after*: Amsterdam event calendars and tourism event datasets (e.g., IAmsterdam events database)

**Weather**: Daily weather data with temperature, precipitation, humidity.
- *Modeled after*: OpenWeatherMap historical weather data format and KNMI (Royal Netherlands Meteorological Institute) weather datasets

**Bus Schedules**: Bus routes and schedules for Amsterdam.
- *Modeled after*: GTFS (General Transit Feed Specification) format used by public transport agencies worldwide, including GVB Amsterdam transit data

**Bookings**: Generated day by day. Base bookings per day multiplied by event intensity and weather factors. Guest pool reused with dynamic repeat probability:
- Base: 30% chance of repeat guest
- After recommendations start: Treatment guests maintain 30% repeat rate, control guests drop to ~9% (70% chance to create new guest instead). This models retention impact of recommendations.
- *Modeled after*: Hotel booking datasets (e.g., Expedia hotel bookings dataset on Kaggle, Airbnb booking datasets)

**Web Analytics**: Generated from bookings. Recommendations shown 1-7 days before booking date. Control group (20% of guests) excluded from recommendations. Conversion rate calculated based on click and conversion probabilities.
- *Modeled after*: E-commerce recommendation tracking datasets (e.g., RetailRocket recommendation dataset, Amazon product recommendation datasets)

**Additional Bookings**: Generated from converted guests after web analytics generation. Dynamic conversion rate:
- Before recommendations start: 5% of conversions lead to bookings
- After recommendations start: 15% of conversions lead to bookings (3x boost)
Simulates direct conversion impact of recommendations.

## Configuration

Key parameters in `config.py`:

**Dataset Generation:**
- `DATASET_START_DATE`, `DATASET_END_DATE` - Date range for datasets
- `DATASET_BASE_BOOKINGS_PER_DAY` - Base number of bookings per day
- `RECOMMENDATION_START_DATE` - When recommendations begin (for impact measurement)
- `CONTROL_GROUP_PERCENTAGE` - Percentage of guests in control group (default: 20%)

**Dataset Generation - Impact Simulation:**
- `BASE_REPEAT_PROBABILITY` - Base probability of repeat guest booking (default: 0.3)
- `CONTROL_RETENTION_DROP` - Control group retention drop probability (default: 0.7)
- `CONVERSION_BASE_RATE` - Base conversion rate for additional bookings (default: 0.05)
- `CONVERSION_BOOST_RATE` - Boosted conversion rate after recommendations (default: 0.15)
- `BASE_CLICK_RATE` - Base click rate for recommendations (default: 0.15)
- `BASE_CONVERSION_RATE` - Base conversion rate for web analytics (default: 0.08)

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Starts API server (port 8000) and dashboard (port 8501).

### Dashboard Tabs

- EDA - Data analysis
- Forecast - Demand and RevPAR forecasts
- Recommendations - Event recommendations (default: next 10 days)
- Itinerary - Event itinerary
- Impact - Conversion rate, A/B test, and causal impact (DID) metrics

### API Endpoints

- `GET /forecast/demand?periods=30`
- `GET /forecast/revpar?periods=30`
- `GET /recommend/{guest_id}?n=5`
- `GET /itinerary/{guest_id}?days=3&n_per_day=3`

## Methodology

- **Forecasting**: Prophet with event intensity, weather, temporal features
- **Recommendations**: Hybrid (collaborative + content-based filtering) with K-means personas
- **Impact Measurement**: 
  - **Conversion Rate**: Percentage of recommendations that convert
  - **A/B Test**: Treatment vs control group comparison after recommendations start (bookings per guest)
  - **Difference-in-Differences (DID)**: Causal impact accounting for natural trends by comparing treatment and control changes over time

## Dataset References

The synthetic datasets in this project were modeled after the following real-world datasets:

- **Bookings**: Hotel booking datasets (e.g., Expedia hotel bookings dataset on Kaggle, Airbnb booking datasets) - https://www.kaggle.com/datasets
- **Events**: Amsterdam event calendars and tourism event databases (e.g., IAmsterdam events database) - https://www.iamsterdam.com/en/see-and-do/whats-on
- **Weather**: OpenWeatherMap historical weather data format and KNMI (Royal Netherlands Meteorological Institute) weather datasets - https://openweathermap.org/api, https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script
- **Bus Schedules**: GTFS (General Transit Feed Specification) format used by public transport agencies, including GVB Amsterdam transit data - https://gtfs.org/, https://gtfs.ovapi.nl/
- **Web Analytics**: E-commerce recommendation tracking datasets (e.g., RetailRocket recommendation dataset, Amazon product recommendation datasets) - https://www.kaggle.com/datasets

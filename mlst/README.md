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

Generate datasets:
```bash
python generate_all_datasets.py
```

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
- Impact - Conversion rate and booking metrics

### API Endpoints

- `GET /forecast/demand?periods=30`
- `GET /forecast/revpar?periods=30`
- `GET /recommend/{guest_id}?n=5`
- `GET /itinerary/{guest_id}?days=3&n_per_day=3`

## Methodology

- **Forecasting**: Prophet with event intensity, weather, temporal features
- **Recommendations**: Hybrid (collaborative + content-based filtering) with K-means personas
- **Impact**: Conversion rate and booking improvement

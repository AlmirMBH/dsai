# Tourism & Smart City Analytics

**Course:** Machine Learning: Supervised Techniques  
**Professor:** Amila Akagic  
**Authors:** Rijalda Sacirbegovic, Almir Mustafic, Benjamin Kljuno

## Overview

This project implements a tourism analytics system for Amsterdam that combines forecasting and recommendations. The system forecasts city-level tourism demand and Revenue Per Available Room (RevPAR) while providing personalized event recommendations based on guest personas.

## Problem Statement

Tourism is seasonal and uneven, which is challenging for businesses. Small and medium enterprises (SMEs) struggle to predict demand and optimize staffing, inventory, and pricing. Additionally, visitors often receive generic itineraries that do not match their interests, budgets, or preferences.

## Objectives

- **Forecast city/region demand and RevPAR** using time-series forecasting models
- **Recommend personalized itineraries/tours per persona** using collaborative and content-based filtering
- **Measure impact on bookings** through conversion rate tracking and before/after comparisons

## Datasets

The project uses synthetic Amsterdam-focused datasets spanning November 2023 to November 2025. At this stage, we were not able to find appropriate real datasets that meet our requirements. Therefore, the existing datasets were generated using custom Python scripts in the `dataset_generators/` directory, which were developed based on patterns from the Kaggle Hotel Booking Demand Dataset (2015-2017, "City Hotel"/"Resort Hotel").

The generated datasets include:

- **bookings.csv** - Accommodation bookings with guest information, dates, rooms booked, ADR, and RevPAR
- **events.csv** - Amsterdam events (concerts, festivals, conferences) with attendance estimates
- **weather.csv** - Daily weather data (temperature, precipitation, humidity)
- **bus_schedules.csv** - GVB bus schedules with routes and stops

All datasets are date-aligned and Amsterdam-specific. See `dataset_generators/README_DATASETS.md` for detailed dataset information and generation instructions.

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd MLST
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generate Datasets

If datasets are not present, generate them using:

```bash
cd dataset_generators
python generate_all_datasets.py
```

This generates all datasets in the correct order (weather → events → bus_schedules → bookings).

### Run Main Pipeline

Execute the complete pipeline:

```bash
python main.py
```

This will:
- Load and preprocess data
- Train forecasting models
- Generate recommendations
- Calculate impact metrics

### Launch Dashboard

Start the Streamlit dashboard for interactive exploration:

```bash
streamlit run dashboard.py
```

The dashboard includes:
- **EDA Tab**: Exploratory data analysis visualizations
- **Forecast Tab**: Demand and RevPAR forecasts
- **Recommendations Tab**: Personalized event recommendations
- **Impact Tab**: Conversion rate and booking improvement metrics

### API Server

Start the FastAPI server:

```bash
uvicorn api:app --reload
```

API endpoints:
- `GET /forecast/demand?periods=30` - Demand forecast
- `GET /forecast/revpar?periods=30` - RevPAR forecast
- `GET /recommend/{guest_id}?n=5` - Event recommendations for a guest

## Project Structure

```
MLST/
├── ingest.py              # Data loading
├── preprocess.py          # Data cleaning and aggregation
├── forecast.py            # Prophet forecasting model
├── personas.py            # Guest persona clustering
├── recommend.py           # Event recommendation system
├── impact.py              # Impact measurement
├── api.py                 # FastAPI endpoints
├── dashboard.py           # Streamlit dashboard
├── main.py                # Main execution script
├── requirements.txt       # Python dependencies
├── datasets/              # CSV data files
└── dataset_generators/    # Dataset generation scripts
```

## Methodology

### Forecasting

- **Model**: Prophet with exogenous regressors (event intensity, rain flag, temperature)
- **Targets**: Daily demand (rooms sold) and RevPAR
- **Features**: Event intensity, weather indicators, temporal features (day of week, month)

### Recommendations

- **Approach**: Hybrid recommendation system combining:
  - **Collaborative filtering**: User-item matrix based on booking patterns, finding similar users via cosine similarity
  - **Content-based filtering**: TF-IDF on event attributes (type, name, location)
- **Personas**: K-means clustering (k=3) based on guest age, average daily rate, and booking frequency
- **Input**: Guest ID or persona ID
- **Output**: Top-N event recommendations

### Impact Measurement

- Conversion rate: Bookings from recommendations / Total recommendations shown
- Booking improvement: Average bookings with recommendations vs. without

## Results

The system provides:
- **Forecast dashboards** showing demand and RevPAR predictions
- **Itinerary API** for personalized event recommendations
- **Impact metrics** tracking conversion rates and booking improvements

Expected outcomes include 5-10% conversion improvement on partner sites and better resource planning for hotels and event organizers.

## Sustainability & Societal Impact

- Promotes balanced visitor distribution and reduces over-tourism
- Supports local small businesses (SMEs) through better demand forecasting
- Uses only aggregate, anonymized data; no personal data collected

## License

This project is part of an academic course assignment.

## Contact

For questions or issues, please contact the project authors.


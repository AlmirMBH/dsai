# Tourism & Smart City Analytics

**Course:** Machine Learning: Supervised Techniques  
**Professor:** Amila Akagic  
**Authors:** Rijalda Sacirbegovic, Almir Mustafic, Benjamin Kljuno

## Project Background

This project was completed as part of the Machine Learning: Supervised Techniques course. The system implements a tourism analytics system for Amsterdam that forecasts demand and RevPAR, and recommends events per persona. It uses time series forecasting (Prophet), hybrid recommendation systems (collaborative + content-based filtering), and causal impact measurement (A/B testing, difference-in-differences).

## Technologies

The system is built using Python and the following libraries:

- **pandas**: Data manipulation and analysis
- **prophet**: Time series forecasting
- **scikit-learn**: Machine learning (K-means clustering for personas, similarity calculations)
- **fastapi**: REST API framework
- **uvicorn**: ASGI server
- **streamlit**: Web dashboard
- **matplotlib**: Data visualization

## Setup Virtual Environment

```bash
python3 -m venv venv
```

## Project Installation
```bash
source venv/bin/activate && pip install -r requirements.txt
```

## Generate Datasets (Mandatory)
```bash
cd dataset_generators && python generate_all_datasets.py
```

## Start Project
```bash
source venv/bin/activate && python main.py
```

Starts API server (port 8000) and dashboard (port 8501).

## Project Startup Note
The first time the project is run, loading the datasets and performing initial evaluations may take 2–3 minutes before the project is fully operational. 


## Stop the project
```
pkill -f streamlit
```

### Application Flow

**Data Pipeline (before running main.py):**

1. **Dataset Generation** (`dataset_generators/generate_all_datasets.py`)
   - Generates datasets: weather, events, bus_schedules, bookings, web_analytics
   - Generates additional bookings from conversions
   - **Dataset Pollution** (`dataset_generators/dataset_polluter.py`): Introduces data issues (missing values, type errors, outliers, duplicates, invalid values) at 5% rate if enabled in config.py
   - Saves polluted datasets to `datasets/` directory

**When `main.py` runs:**

1. **Server Startup**
   - FastAPI server starts (port 8000)
   - Streamlit dashboard starts (port 8501)

2. **Data Ingestion** (`data_ingestion.py`)
   - Dashboard tabs call `data_ingestion.get_data()`
   - Raw CSV files are loaded from `datasets/`
   - **Data Cleaning** (`data_cleaning.py`) is applied:
     - Remove duplicates
     - Fix invalid values and type errors
     - Handle outliers
     - Impute missing values (median or seasonal mean)
   - Cleaned data is cached

3. **Data Processing (per tab)**
   - **Data Processing Tab**: Shows data quality metrics and cleaning operations
   - **EDA Tab**: Shows trends and transport analysis (bus activity vs demand)
   - **Forecast Tab**: Runs Prophet forecasting with events, weather, and bus trips
   - **Impact Tab**: Measures conversion and A/B test results using deterministic groups
   - **Recommendations Tab**: Shows persona-aware event recommendations
   - **Itinerary Tab**: Shows daily events and suggested bus routes

4. **API Endpoints**
   - Use same cleaned data
   - Return forecast, recommendations, and itineraries with transport info

**Note**: Datasets must be generated before starting the application. If datasets are missing, the dashboard displays an error message.

## Stop Project

Stop: `pkill -f "python main.py"` or `Ctrl+C`

## Configuration File

The `config.py` file contains system settings.

**Dataset Paths:**
- `DATASETS_PATH` - Path to datasets directory (default: `datasets/`)
- `BOOKINGS_FILE` - Path to bookings CSV file (default: `datasets/bookings.csv`)
- `EVENTS_FILE` - Path to events CSV file (default: `datasets/events.csv`)
- `WEATHER_FILE` - Path to weather CSV file (default: `datasets/weather.csv`)

**Application Settings:**
- `API_PORT` - API server port (default: 8000)
- `DASHBOARD_PORT` - Dashboard server port (default: 8501)
- `DEFAULT_FORECAST_PERIODS` - Default forecast periods (default: 30)
- `DEFAULT_RECOMMENDATIONS` - Default number of recommendations (default: 5)
- `DEFAULT_RECOMMENDATION_DAYS` - Default recommendation date range in days (default: 10)
- `DEFAULT_EVENTS_PER_DAY` - Default events per day for itinerary (default: 3)

**Dataset Generation:**
- `DATASET_START_DATE`, `DATASET_END_DATE` - Date range for datasets
- `DATASET_BASE_BOOKINGS_PER_DAY` - Base number of bookings per day
- `RECOMMENDATION_START_DATE` - When recommendations begin (for impact measurement)
- `CONTROL_GROUP_PERCENTAGE` - Percentage of guests in control group (default: 0.2 = 20%)

**Impact Simulation:**
- `BASE_REPEAT_PROBABILITY` - Base probability of repeat guest booking (default: 0.3)
- `CONTROL_RETENTION_DROP` - Control group retention drop probability (default: 0.7)
- `CONVERSION_BOOST_RATE` - Conversion rate after recommendations (default: 0.15)
- `BASE_CLICK_RATE` - Base click rate for recommendations (default: 0.15)
- `BASE_CONVERSION_RATE` - Base conversion rate for web analytics (default: 0.08)

**Dataset Pollution:**
- `ENABLE_DATASET_POLLUTION` - Enable/disable dataset pollution (default: True)
- `POLLUTION_TARGET_RATE` - Target total pollution rate per dataset (default: 0.05 = 5%)
- `POLLUTION_OUTLIER_RATE` - Outlier pollution rate (default: 0.015 = 1.5%)
- `POLLUTION_DUPLICATE_RATE` - Duplicate row rate (default: 0.015 = 1.5%)

**Recommendation System:**
- `PERSONAS_CLUSTERS` - Number of persona clusters for K-means (default: 3)
- `SIMILAR_USERS_COUNT` - Number of similar users for collaborative filtering (default: 10)
- `RANDOM_STATE` - Random seed for reproducibility (default: 42)

After making any changes to `config.py`, restart the application to apply the changes.

## Dataset

Synthetic Amsterdam datasets (dates defined in `config.py`):
- bookings.csv - Accommodation bookings
- events.csv - Amsterdam events
- weather.csv - Daily weather data
- bus_schedules.csv - Bus schedules
- web_analytics.csv - Recommendation tracking data

Generate datasets:
```bash
python dataset_generators/generate_all_datasets.py
```

**Note:** Datasets are polluted with data issues (missing values, type errors, outliers, duplicates, invalid values) at 5% rate across all datasets.

### Dataset Generation

Datasets are generated in order: weather, events, bus schedules, bookings, web analytics, additional bookings.

**Events**: At least one event per day. Seasonal patterns (more in summer, weekends). Annual events included.
- *Modeled after*: Amsterdam event calendars (e.g., IAmsterdam events database)

**Weather**: Daily weather data with temperature, precipitation, humidity.
- *Modeled after*: OpenWeatherMap and KNMI weather datasets

**Bus Schedules**: Bus routes and schedules for Amsterdam.
- *Modeled after*: GTFS format (GVB Amsterdam transit data)

**Bookings**: Generated day by day. Base bookings per day multiplied by event intensity and weather factors. Guest pool reused with repeat probability:
- Base: 30% chance of repeat guest
- After recommendations start: Treatment guests maintain 30% repeat rate, control guests (determined by `guest_id % 100 < 20`) drop to ~9% (70% chance to create new guest instead)
- *Modeled after*: Hotel booking datasets (Expedia, Airbnb)

**Web Analytics**: Generated from bookings. Recommendations shown 1-7 days before booking date. Control group (based on deterministic assignment) excluded from recommendations.
- *Modeled after*: E-commerce recommendation tracking datasets (RetailRocket, Amazon)

**Additional Bookings**: Generated from converted guests after web analytics generation:
- Intentional Design: Only existing guests (past bookers) receive recommendations and can generate additional bookings. This simulates targeted marketing to a registered guest database.
- Impact: Converted recommendations have a 15% chance (`CONVERSION_BOOST_RATE`) of leading to a return booking.

## Methodology

- **Forecasting**: Prophet with event intensity, weather, bus trip counts, and temporal features
- **Recommendations**: Hybrid (collaborative + content-based filtering) with K-means personas. Collaborative filtering is persona-aware.
- **Impact Measurement**: 
  - **Conversion Rate**: Percentage of recommendations that convert
  - **A/B Test**: Treatment vs control group comparison (bookings per guest)
  - **Difference-in-Differences (DID)**: Causal impact accounting for trends
  - **Deterministic Assignment**: Control groups are assigned based on `guest_id % 100`. This ensures consistent group membership across all scripts without external state.

## Data Processing Pipeline

6-phase data cleaning pipeline:

1. **Data Ingestion** - Load raw datasets from CSV files
2. **EDA** - Exploratory data analysis and transport analysis
3. **Data Cleaning** - Remove duplicates, fix invalid values, handle outliers
4. **Data Imputation & Standardization** - Fill missing values (median for numeric, "Unknown" for categorical). Forecast uses seasonal mean imputation.
5. **Quality Metrics & Validation** - Calculate completeness, track cleaning operations
6. **Final Display** - Show before/after statistics in dashboard

**Cleaning Operations:**
- **Bookings**: Remove duplicates, fix invalid dates (departure < arrival), fix negative prices and age outliers, impute missing values
- **Events**: Remove duplicates, fix negative attendance, remove invalid dates, impute missing values
- **Weather**: Remove duplicates, fix negative precipitation, fix temperature outliers, impute missing values
- **Web Analytics**: Remove duplicates, fix invalid date formats, drop rows with missing dates, fix invalid boolean values
- **Bus Schedules**: Remove duplicates, remove invalid dates, impute missing values

Cleaning operations are applied when datasets are loaded via `data_ingestion.get_data()`.

## Frontend

Streamlit web interface accessible at `http://localhost:8501`.

### How to Use the UI

**Data Processing Tab:**
- View data quality metrics for all datasets
- Compare raw vs cleaned datasets
- Review cleaning operations performed
- See before/after visualizations

**EDA Tab:**
- Explore time series trends (rooms sold over time)
- View monthly averages
- Analyze distributions (RevPAR histogram)
- Examine relationships (temperature vs demand)
- Compare event intensity impact

**Forecast Tab:**
- Adjust forecast periods (7-90 days)
- View demand and RevPAR forecasts
- Compare actual vs predicted values

**Impact Tab:**
- View conversion rate
- Compare A/B test results (treatment vs control)
- Review causal impact (difference-in-differences)

**Recommendations Tab:**
- Enter guest ID
- Select number of recommendations
- Choose date range
- View recommended events

**Itinerary Tab:**
- Enter guest ID
- Set events per day
- Choose date range
- View daily event itinerary

### API Endpoints

- `GET /forecast/demand?periods=30`
- `GET /forecast/revpar?periods=30`
- `GET /recommend/{guest_id}?number_of_recommendations=5`
- `GET /itinerary/{guest_id}?start_date=2024-07-01&end_date=2024-07-03`

## Dataset References

Synthetic datasets modeled after:
- **Bookings**: Hotel booking datasets (Expedia, Airbnb) - https://www.kaggle.com/datasets
- **Events**: Amsterdam event calendars (IAmsterdam) - https://www.iamsterdam.com/en/see-and-do/whats-on
- **Weather**: OpenWeatherMap, KNMI weather datasets - https://openweathermap.org/api, https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script
- **Bus Schedules**: GTFS format (GVB Amsterdam) - https://gtfs.org/, https://gtfs.ovapi.nl/
- **Web Analytics**: E-commerce recommendation datasets (RetailRocket, Amazon) - https://www.kaggle.com/datasets

## Known Limitations

- Synthetic datasets may not reflect real-world data distributions 100%
- Forecasting accuracy depends on data quality and temporal patterns
- Recommendation system uses persona clustering
- Impact measurement uses deterministic control/treatment group membership based on guest IDs to ensure consistency.
- Data cleaning pipeline handles common issues but may not cover all edge cases

## Next Steps

- **Evaluation metrics**: Implement precision, recall, RMSE (Root Mean Square Error), and user studies.
- **Scaling improvements**: Migrate from in-memory data structures to persistent databases.
- **Algorithm enhancements**: Explore matrix factorization (e.g. SVD) and deep learning methods.
- **Feature enhancements**: Integrate user feedback mechanisms, support real-time booking updates, and implement A/B testing for algorithm comparison.
- **Performance optimizations**: Implement parallel processing for similarity calculations and add incremental updates to avoid full recomputation when new bookings are added.

## Contact

For questions or collaboration, please reach out to:

- Almir Mustafic — [GitHub](https://github.com/AlmirMBH)
- Rijalda Sacirbegovic
- Benjamin Kljuno

## License

This project is licensed under the MIT License.

## Acknowledgments

This project uses the following third-party libraries, datasets, and services:

- **pandas**: BSD License
- **prophet**: MIT License
- **scikit-learn**: BSD License
- **fastapi**: MIT License
- **uvicorn**: BSD License
- **streamlit**: Apache License 2.0
- **matplotlib**: Matplotlib License (BSD-compatible)

Special thanks to Professor Amila Akagic for guidance and supervision during the course.

## Disclaimer

The synthetic datasets used in this project are for educational and demonstration purposes only. This project is an academic exercise completed as part of the Machine Learning: Supervised Techniques course and does not represent a production analytics system.

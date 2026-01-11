# Amsterdam Dataset Generators

This directory contains scripts to generate synthetic datasets for the MLST project, all focused on Amsterdam. The date range is controlled by `DATASET_START_DATE` and `DATASET_END_DATE` in `config.py`.

## Datasets Generated

1. **events.csv** - Amsterdam events (concerts, festivals, conferences, etc.)
2. **weather.csv** - Amsterdam weather data (temperature, precipitation, humidity)
3. **bus_schedules.csv** - GVB bus schedules with time-of-day
4. **bookings.csv** - Hotel/accommodation bookings correlated with events and weather
5. **web_analytics.csv** - Recommendation tracking data (clicks, conversions)

## Quick Start

### Generate All Datasets

```bash
python generate_all_datasets.py
```

This generates all datasets in a mandatory sequence to maintain logical dependencies:
1. **Weather & Events** (`generate_weather.py`, `generate_events.py`): Creates the city foundation (climate and activity).
2. **Bus Schedules** (`generate_bus_schedules.py`): Links transport to the venues created in Step 1.
3. **Base Bookings** (`generate_bookings.py`): Uses the foundation data to simulate natural hotel demand.
4. **Web Analytics** (`generate_web_analytics.py`): Suggests events to those guests and tracks engagement.
5. **Success Bookings** (`generate_bookings.py`): Simulates return trips for guests who converted on suggestions.
6. **Data Pollution** (`dataset_polluter.py`): Corrupts 5% of the final data to test cleaning tools.

### Generate Individual Datasets

#### Events
```bash
python generate_events.py
```

#### Weather
```bash
python generate_weather.py
```

#### Bus Schedules
```bash
python generate_bus_schedules.py
```

#### Bookings
```bash
python generate_bookings.py
```

Bookings should be generated after events and weather to enable correlations.

## Generation Logic

### Step 1: Climate & Events
- **Climate & Events**: Generates the weather using a Sine-Wave and city events using a Poisson rule. The Sine-Wave formula creates natural temperature cycles (hot summers, cold winters), while the Poisson rule ensures the number of events per day varies naturally (some days have 0, others have 5). Expected event attendance is rounded to the nearest 100 to look realistic. This happens in `generate_weather.py` and `generate_events.py`.

### Step 2: Transport
- **Transport**: Creates bus routes and stops that share the same names as the city venues created in Step 1. It generates a realistic schedule where buses arrive every 7 minutes during the "Morning Rush" but only every 25 minutes late at night. The schedule is static and does not change for city events or seasons. This happens in `generate_bus_schedules.py`.

### Step 3: Base Bookings
- **Base Bookings**: Creates Base Bookings of the hotel data using Demand Scaling and Loyalty Selection. The system starts with 100 base bookings per day and then multiplies that number based on Step 1. For example, it adds +25% if a festival is happening and +15% if the weather is sunny. The system also simulates loyalty by keeping a "Guest Pool" in its memory; for every new booking, it has a 30% chance to reuse a guest who has already visited instead of creating a new one. This represents guests who visit the hotel naturally due to city events or seasons, independent of the recommendation system. This happens in `generate_bookings.py`.

### Step 4: Simulated Analytics
- **Simulated Analytics**: Simulates guests engaging with the recommendation system. It uses the Deterministic Group Assignment rule (ID % 100) to split guests into a 20% Control group (who see nothing) and an 80% Treatment group. For the Treatment group, it records simulated "clicks" and "conversions" based on how well the event matches their stay dates. This happens in `generate_web_analytics.py`.

### Step 5: Success Bookings
- **Success Bookings**: Creates Success Bookings (based on recommendations) of the hotel data. It looks at the "converted" guests from Step 4 and gives them a 15% chance (Conversion Boost Rate) of booking a return trip. These represent the extra sales specifically caused by the AI recommendations. This happens in `generate_bookings.py`.

### Step 6: Data Pollution
- **Data Pollution**: Adds errors to the files until exactly 5% of all data is corrupted, which matches real-world averages for dirty data. It adds 1.5% outliers (like 200-year-old guests), 1.5% duplicate records, and 2% missing values (NaN). This allows the system to test the quality of the cleaning tools. This happens in `dataset_polluter.py`.

## Dataset Details

### Events Dataset

**Columns:**
- `id` - Event identifier
- `date` - Event date (YYYY-MM-DD)
- `time` - Event time (HH:MM format)
- `type` - Event type (concert, festival, conference, etc.)
- `name` - Event name
- `location` - Event location/venue
- `expected_attendance` - Number of attendees

### Weather Dataset

**Columns:**
- `date` - Weather date (YYYY-MM-DD)
- `temperature_max` - Maximum temperature (°C × 10)
- `temperature_min` - Minimum temperature (°C × 10)
- `weather_category` - Weather type (sunny, rainy, cloudy, etc.)
- `precipitation` - Rainfall in mm
- `humidity` - Humidity percentage

### Bus Schedules Dataset

**Columns:**
- `id` - Unique trip identifier
- `date` - Schedule date (YYYY-MM-DD)
- `time` - Arrival time (HH:MM)
- `route_id` - Bus route identifier
- `stop_id` - Stop identifier
- `stop_name` - Stop name with location

### Bookings Dataset

**Columns:**
- All 27 columns as specified (id, uuid, accommodation_id, etc.)
- `date` - Booking date
- `arrival_date` - Check-in date
- `departure_date` - Check-out date
- Guest information (first_name, last_name, email, age, country)
- Accommodation details (Amsterdam addresses only)

## Data Consistency

All datasets:
- Share the same date range (configurable in `config.py`)
- Focus on Amsterdam only
- Are date-aligned for easy joins
- Use consistent date formats (YYYY-MM-DD)

## Dependencies

```bash
pip install pandas numpy
```

## Example Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Generate all datasets
python generate_all_datasets.py

# Or generate individually (in order)
python generate_weather.py
python generate_events.py
python generate_bus_schedules.py
python generate_bookings.py  # This uses events.csv and weather.csv
```

## Dataset Pollution

Datasets are automatically polluted with data quality issues (missing values, type errors, outliers, duplicates, invalid values) at a 5% rate. This is controlled by `ENABLE_DATASET_POLLUTION` in `config.py`. The pollution is applied by `dataset_polluter.py` after all clean datasets are generated.

## Notes

- All scripts use random seed 42 for reproducibility
- Bookings generation requires events.csv and weather.csv to be present for correlations
- If events/weather files are missing, bookings will still generate but without correlations
- Web analytics generation requires bookings.csv to be present
- All datasets are saved as CSV files in the `datasets/` directory
- Dataset pollution is applied automatically if enabled in config.py


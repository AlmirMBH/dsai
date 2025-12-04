# Amsterdam Dataset Generators

This directory contains scripts to generate synthetic datasets for the MLST project, all focused on Amsterdam and spanning November 2023 - November 2025.

## Datasets Generated

1. **events.csv** - Amsterdam events (concerts, festivals, conferences, etc.)
2. **weather.csv** - Amsterdam weather data (temperature, precipitation, humidity)
3. **bus_schedules.csv** - GVB bus schedules with time-of-day
4. **bookings.csv** - Hotel/accommodation bookings correlated with events and weather

## Quick Start

### Generate All Datasets (Recommended)

```bash
python generate_all_datasets.py
```

This will generate all datasets in the correct order:
1. Weather (foundation)
2. Events
3. Bus Schedules
4. Bookings (correlated with events & weather)

### Generate Individual Datasets

#### Events
```bash
python generate_events.py
```

Options:
- `--start-date YYYY-MM-DD` (default: 2023-11-01)
- `--end-date YYYY-MM-DD` (default: 2025-11-30)
- `--output events.csv` (default: events.csv)

#### Weather
```bash
python generate_weather.py
```

Options:
- `--start-date YYYY-MM-DD` (default: 2023-11-01)
- `--end-date YYYY-MM-DD` (default: 2025-11-30)
- `--output weather.csv` (default: weather.csv)

#### Bus Schedules
```bash
python generate_bus_schedules.py
```

Options:
- `--start-date YYYY-MM-DD` (default: 2023-11-01)
- `--end-date YYYY-MM-DD` (default: 2025-11-30)
- `--output bus_schedules.csv` (default: bus_schedules.csv)

#### Bookings
```bash
python generate_bookings.py
```

**Important:** Bookings should be generated AFTER events and weather to enable correlations.

Options:
- `--start-date YYYY-MM-DD` (default: 2023-11-01)
- `--end-date YYYY-MM-DD` (default: 2025-11-30)
- `--n-accommodations N` (default: 50)
- `--events-file events.csv` (default: events.csv)
- `--weather-file weather.csv` (default: weather.csv)
- `--output bookings.csv` (default: bookings.csv)

## Dataset Details

### Events Dataset

**Columns:**
- `event_id` - Unique event identifier
- `date` - Event date (YYYY-MM-DD)
- `type` - Event type (concert, festival, conference, etc.)
- `name` - Event name
- `location` - Event location/venue
- `expected_attendance` - Estimated number of attendees

**Features:**
- Includes major Amsterdam events:
  - King's Day (April 27)
  - Amsterdam Dance Event (ADE) - October
  - Amsterdam Pride - August
  - Amsterdam Marathon - October
  - Amsterdam Light Festival - December
- More events on weekends and in summer
- Real Amsterdam venues (Ziggo Dome, RAI Amsterdam, etc.)

### Weather Dataset

**Columns:**
- `date` - Weather date (YYYY-MM-DD)
- `temperature_max` - Maximum temperature (°C × 10)
- `temperature_min` - Minimum temperature (°C × 10)
- `weather_category` - Weather type (sunny, rainy, cloudy, etc.)
- `precipitation` - Rainfall in mm
- `humidity` - Humidity percentage

**Features:**
- Realistic Amsterdam maritime climate
- Seasonal temperature patterns
- Realistic precipitation patterns
- Humidity included

### Bus Schedules Dataset

**Columns:**
- `trip_id` - Unique trip identifier
- `date` - Schedule date (YYYY-MM-DD)
- `time` - Arrival time (HH:MM)
- `route_id` - Bus route identifier
- `stop_id` - Stop identifier
- `stop_name` - Stop name with location

**Features:**
- Real GVB routes (Lines 15, 18, 21, 22, 24, 26, 48, 65)
- Real Amsterdam stops (Centraal Station, Dam, Leidseplein, etc.)
- Time-of-day included
- More trips on weekdays
- Operating hours: 05:30 - 00:30

### Bookings Dataset

**Columns:**
- All 27 columns as specified (id, uuid, accommodation_id, etc.)
- `date` - Booking date
- `arrival_date` - Check-in date
- `departure_date` - Check-out date
- Guest information (first_name, last_name, email, age, country)
- Accommodation details (Amsterdam addresses only)

**Features:**
- Amsterdam addresses only
- Guests from around the world
- Correlated with events (more bookings during major events)
- Correlated with weather (more bookings in good weather)
- 50-200 bookings per day (varies based on events/weather)
- Real Amsterdam street names and districts

## Data Consistency

All datasets:
- Share the same date range: 2023-11-01 to 2025-11-30
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

## Notes

- All scripts use random seed 42 for reproducibility
- Bookings generation requires events.csv and weather.csv to be present for correlations
- If events/weather files are missing, bookings will still generate but without correlations
- All datasets are saved as CSV files in the current directory


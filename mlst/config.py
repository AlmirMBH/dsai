import os

# INFRASTRUCTURE (Paths & Ports)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = 'datasets'
DATASETS_PATH = os.path.join(PROJECT_ROOT, DATASETS_DIR)
BOOKINGS_FILE = f'{DATASETS_DIR}/bookings.csv'
EVENTS_FILE = f'{DATASETS_DIR}/events.csv'
WEATHER_FILE = f'{DATASETS_DIR}/weather.csv'
WEB_ANALYTICS_FILE = f'{DATASETS_DIR}/web_analytics.csv'
BUS_SCHEDULES_FILE = f'{DATASETS_DIR}/bus_schedules.csv'

API_PORT = 8000
DASHBOARD_PORT = 8501

# DATA GENERATION (World Simulation & Pollution)
# City/region for generated data (addresses, locations, stop names); change to support any city
CITY_NAME = 'Amsterdam'
COUNTRY_NAME = 'Netherlands'
DATASET_START_DATE = '2024-01-01' # Earliest date for generated datasets
DATASET_END_DATE = '2026-10-01' # Latest date for generated datasets
DATASET_N_ACCOMMODATIONS = 50 # Number of accomodations to create
DATASET_BASE_BOOKINGS_PER_DAY = 100 # Average bookings per day
DATASET_MIN_BOOKINGS_PER_DAY = 50 # Lowest allowed bookings per day
DATASET_MAX_BOOKINGS_PER_DAY = 200 # Highest allowed bookings per day

# Experiment & Behavior Logic
RECOMMENDATION_START_DATE = '2024-06-01' # Date when recommendations start in web_analytics.csv
CONTROL_GROUP_PERCENTAGE = 0.2 # Percentage of guests who get no recommendations
BASE_REPEAT_PROBABILITY = 0.3 # Chance of a guest booking a second or more trip
CONTROL_RETENTION_DROP = 0.7 # Chance to skip a repeat booking for control guests
CONVERSION_BOOST_RATE = 0.15 # Chance a converted recommendation becomes a physical booking
BASE_CLICK_RATE = 0.15 # Percentage of recommendations that are clicked
BASE_CONVERSION_RATE = 0.08 # Percentage of clicks that are converted
EVENT_ATTENDANCE_MAX = 100000 # Limit for event crowd sizes

# Dataset Pollution
ENABLE_DATASET_POLLUTION = True # Enable data pollution after datasets are generated
POLLUTION_TARGET_RATE = 0.05 # Percentage of corrupted data per dataset
POLLUTION_OUTLIER_RATE = 0.015 # Percentage of records turned into outliers in each dataset
POLLUTION_DUPLICATE_RATE = 0.015 # Percentage of records that are duplicated in each dataset

# APPLICATION RUNTIME (UI, ML & Validation)
# UI Defaults
DEFAULT_FORECAST_PERIODS = 30 # Default days to predict Demand and RevPAR
DEFAULT_RECOMMENDATIONS = 5 # Default number of event recommendations
DEFAULT_EVENTS_PER_DAY = 3 # Default events per day in itinerary
DEFAULT_RECOMMENDATION_DAYS = 10 # Default day range for event searches

# ML Parameters
RANDOM_STATE = 42
PERSONAS_CLUSTERS = 3 # Number of guest categories for K-means
SIMILAR_USERS_COUNT = 10 # Number of neighbors for collaborative filtering

# Data Cleaning & Experimental Constants
GUEST_AGE_MIN = 0 # Youngest allowed guest age
GUEST_AGE_MAX = 120 # Oldest allowed guest age
TEMPERATURE_MIN_THRESHOLD = -200 # Lowest valid temperature (-20°C stored as Celsius * 10)
TEMPERATURE_MAX_THRESHOLD = 400 # Highest valid temperature (40°C stored as Celsius * 10)
DAYS_IN_MONTH_AVERAGE = 30.44 # Conversion factor for monthly calculations

# --- EVENT GENERATION (generate_events.py) ---
# These venues are  picked when generating an event
EVENTS_VENUES_BY_TYPE = {
    'concert': ['Ziggo Dome', 'AFAS Live', 'Paradiso', 'Melkweg', 'Concertgebouw', 'TivoliVredenburg'],
    'festival': ['Vondelpark', 'Westerpark', 'Museumplein', 'Dam Square', 'RAI Amsterdam', 'NDSM Werf'],
    'conference': ['RAI Amsterdam', 'Beurs van Berlage', 'Amsterdam RAI', 'WTC Amsterdam'],
    'exhibition': ['Rijksmuseum', 'Van Gogh Museum', 'Stedelijk Museum', 'Rembrandt House', 'Anne Frank House', 'NEMO Science Museum'],
    'sports': ['Johan Cruyff Arena', 'Olympic Stadium', 'Ziggo Dome', 'AFAS Live'],
    'education': ['University of Amsterdam', 'VU Amsterdam', 'Amsterdam University College', 'Openbare Bibliotheek Amsterdam'],
    'music': ['Paradiso', 'Melkweg', 'Bitterzoet', 'Sugarfactory', 'De School', 'Shelter'],
    'arts': ['Stedelijk Museum', 'Rijksmuseum', 'FOAM Photography Museum', 'EYE Film Museum', 'Moco Museum'],
    'theater': ['Carré Theatre', 'Stadsschouwburg', 'DeLaMar Theatre', 'Royal Theatre'],
    'comedy': ['Boom Chicago', 'Comedy Café', 'Toomler', 'Comedy Theater']
}

EVENTS_TYPES = ['concert', 'festival', 'conference', 'exhibition', 'sports', 'education', 'music', 'arts', 'theater', 'comedy']

# These names are used when generating an event name
EVENTS_DISPLAY_NAMES_BY_TYPE = {
    'concert': ['Rock Concert', 'Jazz Night', 'Classical Performance', 'Pop Music Show', 'Electronic Music Night', 'Indie Rock Show'],
    'festival': ['Food & Wine Festival', 'Cultural Festival', 'Film Festival', 'Art Festival', 'Music Festival', 'Street Festival'],
    'conference': ['Tech Summit Amsterdam', 'Business Conference', 'Medical Symposium', 'Education Forum', 'Innovation Summit'],
    'exhibition': ['Art Exhibition Opening', 'Photography Show', 'Historical Display', 'Science Exhibition', 'Design Showcase'],
    'sports': ['Ajax Football Match', 'Marathon Race', 'Tennis Tournament', 'Basketball Game', 'Cycling Event', 'Running Event'],
    'education': ['University Open Day', 'Workshop Series', 'Seminar', 'Training Course', 'Educational Fair', 'Lecture Series'],
    'music': ['Live Music Night', 'DJ Set', 'Orchestra Performance', 'Choir Concert', 'Acoustic Session', 'Jazz Session'],
    'arts': ['Theater Performance', 'Dance Show', 'Opera Night', 'Ballet Performance', 'Art Gallery Opening', 'Contemporary Art Show'],
    'theater': ['Drama Play', 'Comedy Show', 'Musical', 'Shakespeare Performance', 'Modern Theater', 'Experimental Theater'],
    'comedy': ['Stand-up Comedy', 'Comedy Night', 'Improv Show', 'Comedy Festival', 'Laugh Out Loud', 'Open Mic Night']
}
# Fixed-date major events (King's Day, Pride, Marathon, Light Festival)
EVENTS_MAJOR_ANNUAL_DATES = {
    '2024-04-27': {'type': 'festival', 'name': "King's Day Celebration", 'venue': 'City-wide', 'attendance': 800000},
    '2024-08-03': {'type': 'festival', 'name': 'Amsterdam Pride Canal Parade', 'venue': 'Canal Route', 'attendance': 500000},
    '2024-10-16': {'type': 'music', 'name': 'Amsterdam Dance Event Opening', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2024-10-20': {'type': 'music', 'name': 'Amsterdam Dance Event Closing', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2024-10-20': {'type': 'sports', 'name': 'Amsterdam Marathon', 'venue': 'Olympic Stadium', 'attendance': 45000},
    '2024-12-01': {'type': 'festival', 'name': 'Amsterdam Light Festival Opening', 'venue': 'Canal Route', 'attendance': 100000},
    '2025-04-27': {'type': 'festival', 'name': "King's Day Celebration", 'venue': 'City-wide', 'attendance': 800000},
    '2025-08-02': {'type': 'festival', 'name': 'Amsterdam Pride Canal Parade', 'venue': 'Canal Route', 'attendance': 500000},
    '2025-10-15': {'type': 'music', 'name': 'Amsterdam Dance Event Opening', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2025-10-19': {'type': 'music', 'name': 'Amsterdam Dance Event Closing', 'venue': 'Multiple Venues', 'attendance': 400000},
    '2025-10-19': {'type': 'sports', 'name': 'Amsterdam Marathon', 'venue': 'Olympic Stadium', 'attendance': 45000},
    '2025-11-30': {'type': 'festival', 'name': 'Amsterdam Light Festival Opening', 'venue': 'Canal Route', 'attendance': 100000},
}

# Major annual festival/music week
EVENTS_ADE_WEEK_START_END_BY_YEAR = {2024: {'start': '2024-10-16', 'end': '2024-10-20'}, 2025: {'start': '2025-10-15', 'end': '2025-10-19'}}

BOOKINGS_GUEST_FIRST_NAMES_POOL = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
    'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
    'Kenneth', 'Carol', 'Kevin', 'Amanda', 'Brian', 'Dorothy', 'George', 'Melissa',
    'Timothy', 'Deborah', 'Ronald', 'Stephanie', 'Jason', 'Rebecca', 'Edward', 'Sharon'
]

BOOKINGS_GUEST_LAST_NAMES_POOL = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
    'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris', 'Sanchez',
    'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
    'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams',
    'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts'
]

BOOKINGS_ACCOMMODATION_TYPES = ['hotel', 'hostel', 'apartment', 'resort', 'villa', 'bed_and_breakfast']

BOOKINGS_CAPACITY_TYPES = ['room', 'bed', 'suite', 'apartment', 'villa', 'house']

BOOKINGS_GUEST_COUNTRIES = [
    'United States', 'United Kingdom', 'Germany', 'France', 'Italy', 'Spain',
    'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Canada', 'Australia',
    'Japan', 'China', 'Brazil', 'Mexico', 'Argentina', 'South Africa', 'India', 'Russia'
]

BOOKINGS_ACCOMMODATION_NAMES = [
    'Grand Hotel Amsterdam', 'Canal View Hotel', 'Rijksmuseum Hotel', 'Dam Square Hotel',
    'Vondelpark Hotel', 'Leidseplein Hotel', 'Jordaan Boutique Hotel', 'Museum Quarter Hotel',
    'Central Station Hotel', 'Anne Frank Hotel', 'Red Light District Hotel', 'Westerpark Hotel',
    'Amsterdam Marriott', 'Hilton Amsterdam', 'NH Collection Amsterdam', 'Park Plaza Amsterdam',
    'Hotel Okura Amsterdam', 'Conservatorium Hotel', 'Pulitzer Amsterdam', 'Waldorf Astoria Amsterdam'
]

BOOKINGS_STREET_NAMES = [
    'Damrak', 'Kalverstraat', 'Nieuwendijk', 'Leidsestraat', 'Rokin', 'Singel',
    'Herengracht', 'Keizersgracht', 'Prinsengracht', 'Jordaan', 'Rozengracht',
    'Overtoom', 'Vondelstraat', 'P.C. Hooftstraat', 'Van Baerlestraat', 'Museumplein',
    'Leidseplein', 'Rembrandtplein', 'Waterlooplein', 'Dam Square', 'Spui',
    'Nieuwezijds Voorburgwal', 'Oudezijds Voorburgwal', 'Warmoesstraat', 'Zeedijk'
]

BOOKINGS_DISTRICTS = ['Centrum', 'Jordaan', 'De Pijp', 'Oud-Zuid', 'Oud-West', 'Westerpark', 'Oost', 'Noord', 'Zuid', 'Nieuw-West']

WEATHER_SEASONAL_PARAMS = {
    'winter': {'avg_temp': 4, 'temp_range': (-2, 10), 'rain_prob': 0.45, 'humidity': (80, 95)},
    'spring': {'avg_temp': 10, 'temp_range': (3, 18), 'rain_prob': 0.30, 'humidity': (70, 85)},
    'summer': {'avg_temp': 19, 'temp_range': (12, 28), 'rain_prob': 0.25, 'humidity': (65, 80)},
    'autumn': {'avg_temp': 12, 'temp_range': (5, 18), 'rain_prob': 0.40, 'humidity': (75, 90)}
}
WEATHER_CONDITION_CATEGORIES = ['sunny', 'partly_cloudy', 'cloudy', 'rainy', 'windy', 'foggy', 'snowy']

BUS_ROUTES = [
    {'route_id': 'R015', 'name': 'Line 15', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'DAM', 'stop_name': 'Dam'}, {'stop_id': 'LEI', 'stop_name': 'Leidseplein'}, {'stop_id': 'MUS', 'stop_name': 'Museumplein'}, {'stop_id': 'VON', 'stop_name': 'Vondelpark'}]},
    {'route_id': 'R018', 'name': 'Line 18', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'DAM', 'stop_name': 'Dam'}, {'stop_id': 'LEI', 'stop_name': 'Leidseplein'}, {'stop_id': 'VON', 'stop_name': 'Vondelpark'}, {'stop_id': 'WES', 'stop_name': 'Westerpark'}]},
    {'route_id': 'R021', 'name': 'Line 21', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'DAM', 'stop_name': 'Dam'}, {'stop_id': 'RAI', 'stop_name': 'RAI Amsterdam'}, {'stop_id': 'ZUI', 'stop_name': 'Amsterdam Zuid'}, {'stop_id': 'SCH', 'stop_name': 'Schiphol Airport'}]},
    {'route_id': 'R022', 'name': 'Line 22', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'WES', 'stop_name': 'Westerpark'}, {'stop_id': 'SLT', 'stop_name': 'Sloterdijk'}, {'stop_id': 'OSD', 'stop_name': 'Osdorp'}]},
    {'route_id': 'R024', 'name': 'Line 24', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'OLY', 'stop_name': 'Olympic Stadium'}, {'stop_id': 'ZUI', 'stop_name': 'Amsterdam Zuid'}]},
    {'route_id': 'R026', 'name': 'Line 26', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'ZUI', 'stop_name': 'Amsterdam Zuid'}, {'stop_id': 'SCH', 'stop_name': 'Schiphol Airport'}]},
    {'route_id': 'R048', 'name': 'Line 48', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'REM', 'stop_name': 'Rembrandtplein'}, {'stop_id': 'MUS', 'stop_name': 'Museumplein'}, {'stop_id': 'VON', 'stop_name': 'Vondelpark'}]},
    {'route_id': 'R065', 'name': 'Line 65', 'stops': [{'stop_id': 'CS', 'stop_name': 'Centraal Station'}, {'stop_id': 'DAM', 'stop_name': 'Dam'}, {'stop_id': 'REM', 'stop_name': 'Rembrandtplein'}, {'stop_id': 'WAT', 'stop_name': 'Waterlooplein'}]}
]

BUS_OPERATING_HOURS_START_END = {'start': 5, 'end': 0}

# 'peak_morning': (7, 9, 7) = (start_hour, end_hour, frequency_minutes)
BUS_SCHEDULE_PATTERNS_WEEKDAY_WEEKEND = {
    'weekday': {'peak_morning': (7, 9, 7), 'midday': (9, 17, 12), 'peak_evening': (17, 19, 8), 'evening': (19, 23, 15), 'late_night': (23, 0, 25)},
    'weekend': {'morning': (6, 10, 15), 'midday': (10, 20, 12), 'evening': (20, 23, 15), 'late_night': (23, 0, 30)}
}

# --- FORECAST (Prophet and LSTM, forecast_prophet.py, forecast_lstm.py) ---
# Standardized regressor column names; must match output of data_ingestion.standardize_regressors
FORECAST_REGRESSORS = [
    "event_intensity_std", "temperature_max_std", "rain_flag", "bus_trip_count_std",
    "event_intensity_lag1_std", "event_intensity_lag7_std", "bus_trip_count_lag1_std", "bus_trip_count_lag7_std",
]
FORECAST_REVPAR_REGRESSORS = FORECAST_REGRESSORS + ["demand_lag1_std", "demand_lag7_std"]

# Prophet
PROPHET_LOGISTIC_MARGIN = 0.15
PROPHET_CHANGEPOINT_PRIOR_SCALE = 0.05
PROPHET_SEASONALITY_PRIOR_SCALE = 10.0

# LSTM: input window length (days), max forecast horizon, calendar feature count, training
LSTM_INPUT_DAYS = 21
LSTM_MAX_HORIZON = 90
LSTM_CALENDAR_COUNT = 5
LSTM_DEFAULT_EPOCHS = 40

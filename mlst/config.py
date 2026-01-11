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
DATASET_START_DATE = '2024-01-01' # Earliest date for generated datasets
DATASET_END_DATE = '2026-02-28' # Latest date for generated datasets
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

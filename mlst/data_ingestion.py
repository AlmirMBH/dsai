import numpy as np
import pandas as pd
import os
import config
from functools import lru_cache
from sklearn.preprocessing import StandardScaler
from data_cleaning import clean_dataset

@lru_cache(maxsize=1)
def load_raw_data():
    """Load raw data from CSV files. Cached."""
    bookings = pd.read_csv(config.BOOKINGS_FILE) if os.path.exists(config.BOOKINGS_FILE) else pd.DataFrame()
    events = pd.read_csv(config.EVENTS_FILE) if os.path.exists(config.EVENTS_FILE) else pd.DataFrame()
    weather = pd.read_csv(config.WEATHER_FILE) if os.path.exists(config.WEATHER_FILE) else pd.DataFrame()
    web_analytics = pd.read_csv(config.WEB_ANALYTICS_FILE) if os.path.exists(config.WEB_ANALYTICS_FILE) else pd.DataFrame()
    bus_schedules = pd.read_csv(config.BUS_SCHEDULES_FILE) if os.path.exists(config.BUS_SCHEDULES_FILE) else pd.DataFrame()
    
    return bookings, events, weather, web_analytics, bus_schedules

@lru_cache(maxsize=1)
def get_data():
    """Load and clean all datasets. Uses cached raw data, caches cleaned result."""
    bookings_raw, events_raw, weather_raw, web_analytics_raw, bus_schedules_raw = load_raw_data()
    
    bookings, _ = clean_dataset(bookings_raw, 'bookings')
    events, _ = clean_dataset(events_raw, 'events')
    weather, _ = clean_dataset(weather_raw, 'weather')
    web_analytics, _ = clean_dataset(web_analytics_raw, 'web_analytics')
    bus_schedules, _ = clean_dataset(bus_schedules_raw, 'bus_schedules')
    
    return bookings, events, weather, web_analytics, bus_schedules

def get_raw_data():
    """Get raw (uncleaned) datasets from cache."""
    return load_raw_data()


def add_lagged_regressors(df: pd.DataFrame) -> pd.DataFrame:
    """Add event_intensity, bus_trip_count, demand at lag 1 and 7. Call before train_test_split."""
    out = df.sort_values("date").reset_index(drop=True).copy()
    out["event_intensity_lag1"] = out["event_intensity"].shift(1)
    out["event_intensity_lag7"] = out["event_intensity"].shift(7)
    out["bus_trip_count_lag1"] = out["bus_trip_count"].shift(1)
    out["bus_trip_count_lag7"] = out["bus_trip_count"].shift(7)
    out["demand_lag1"] = out["demand"].shift(1)
    out["demand_lag7"] = out["demand"].shift(7)
    return out


def train_test_split(df: pd.DataFrame, test_days: int = 30):
    """Last test_days = test, rest = train. Returns train, test, split_date."""
    df = df.sort_values("date").reset_index(drop=True)
    if len(df) < test_days + 1:
        raise ValueError(f"Need at least {test_days + 1} days; got {len(df)}")
    train = df.iloc[:-test_days].copy()
    test = df.iloc[-test_days:].copy()
    split_date = pd.Timestamp(test["date"].min())
    return train, test, split_date


def standardize_regressors(train_df: pd.DataFrame, test_df: pd.DataFrame):
    """Returns train_std, test_std with all regressor columns standardized (including lag columns)."""
    train_std = train_df.copy()
    test_std = test_df.copy()
    scaler_event = StandardScaler()
    train_std["event_intensity_std"] = scaler_event.fit_transform(np.log1p(train_df["event_intensity"].values).reshape(-1, 1)).ravel()
    test_std["event_intensity_std"] = scaler_event.transform(np.log1p(test_df["event_intensity"].values).reshape(-1, 1)).ravel()
    if "event_intensity_lag1" in train_df.columns:
        train_std["event_intensity_lag1_std"] = scaler_event.transform(np.log1p(train_df["event_intensity_lag1"].fillna(0).values).reshape(-1, 1)).ravel()
        test_std["event_intensity_lag1_std"] = scaler_event.transform(np.log1p(test_df["event_intensity_lag1"].fillna(0).values).reshape(-1, 1)).ravel()
        train_std["event_intensity_lag7_std"] = scaler_event.transform(np.log1p(train_df["event_intensity_lag7"].fillna(0).values).reshape(-1, 1)).ravel()
        test_std["event_intensity_lag7_std"] = scaler_event.transform(np.log1p(test_df["event_intensity_lag7"].fillna(0).values).reshape(-1, 1)).ravel()
    scaler_temp = StandardScaler()
    train_std["temperature_max_std"] = scaler_temp.fit_transform(train_df["temperature_max"].values.reshape(-1, 1)).ravel()
    test_std["temperature_max_std"] = scaler_temp.transform(test_df["temperature_max"].values.reshape(-1, 1)).ravel()
    scaler_bus = StandardScaler()
    train_std["bus_trip_count_std"] = scaler_bus.fit_transform(train_df["bus_trip_count"].values.reshape(-1, 1)).ravel()
    test_std["bus_trip_count_std"] = scaler_bus.transform(test_df["bus_trip_count"].values.reshape(-1, 1)).ravel()
    if "bus_trip_count_lag1" in train_df.columns:
        train_std["bus_trip_count_lag1_std"] = scaler_bus.transform(train_df["bus_trip_count_lag1"].fillna(0).values.reshape(-1, 1)).ravel()
        test_std["bus_trip_count_lag1_std"] = scaler_bus.transform(test_df["bus_trip_count_lag1"].fillna(0).values.reshape(-1, 1)).ravel()
        train_std["bus_trip_count_lag7_std"] = scaler_bus.transform(train_df["bus_trip_count_lag7"].fillna(0).values.reshape(-1, 1)).ravel()
        test_std["bus_trip_count_lag7_std"] = scaler_bus.transform(test_df["bus_trip_count_lag7"].fillna(0).values.reshape(-1, 1)).ravel()
    if "demand_lag1" in train_df.columns:
        scaler_demand = StandardScaler()
        scaler_demand.fit(train_df["demand"].values.reshape(-1, 1))
        train_std["demand_lag1_std"] = scaler_demand.transform(train_df["demand_lag1"].fillna(0).values.reshape(-1, 1)).ravel()
        test_std["demand_lag1_std"] = scaler_demand.transform(test_df["demand_lag1"].fillna(0).values.reshape(-1, 1)).ravel()
        train_std["demand_lag7_std"] = scaler_demand.transform(train_df["demand_lag7"].fillna(0).values.reshape(-1, 1)).ravel()
        test_std["demand_lag7_std"] = scaler_demand.transform(test_df["demand_lag7"].fillna(0).values.reshape(-1, 1)).ravel()
    return train_std, test_std
import pandas as pd
import numpy as np
import config

# Set random seed for reproducibility
np.random.seed(config.RANDOM_STATE)

def _calculate_per_column_rate(n_columns, target_rate):
    """Calculate per-column rate to achieve target total pollution rate."""
    if n_columns == 0:
        return 0
    return 1 - (1 - target_rate) ** (1 / n_columns)

def pollute_dataset(df, dataset_type):
    """Introduce real-world data quality issues to datasets."""
    if len(df) == 0:
        return df
    
    df = df.copy()
    n_rows = len(df)
    
    # All datasets: 3 missing + 1 type error + 2 outliers + 1 invalid = 7 pollution applications
    pollution_rate = _calculate_per_column_rate(7, config.POLLUTION_TARGET_RATE)
    
    if dataset_type == 'bookings':
        # Missing values (3 columns)
        missing_cols = [col for col in ['age', 'average_daily_rate', 'guest_country'] if col in df.columns]
        for col in missing_cols:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, col] = np.nan
        
        # Type errors (1 column)
        if 'age' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df['age'] = df['age'].astype(str)
            df.loc[mask, 'age'] = df.loc[mask, 'age'] + ' years'
        
        # Outliers (2 columns)
        if 'age' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'age'] = np.random.randint(121, 200, mask.sum())
        if 'average_daily_rate' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'average_daily_rate'] = -abs(df.loc[mask, 'average_daily_rate'])
        
        # Invalid values (1 type)
        if 'arrival_date' in df.columns and 'departure_date' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'departure_date'] = df.loc[mask, 'arrival_date']
    
    elif dataset_type == 'events':
        # Missing values (3 columns)
        missing_cols = [col for col in ['name', 'location', 'type'] if col in df.columns]
        for col in missing_cols:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, col] = np.nan
        
        # Type errors (1 column)
        if 'name' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df['name'] = df['name'].astype(str)
            df.loc[mask, 'name'] = df.loc[mask, 'name'] + ' event'
        
        # Outliers (2 columns)
        if 'expected_attendance' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'expected_attendance'] = -abs(df.loc[mask, 'expected_attendance'])
        if 'expected_attendance' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'expected_attendance'] = df.loc[mask, 'expected_attendance'] * 1000
        
        # Invalid values (1 type)
        if 'date' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'date'] = '1900-01-01'
    
    elif dataset_type == 'weather':
        # Missing values (3 columns)
        missing_cols = [col for col in ['temperature_max', 'temperature_min', 'precipitation'] if col in df.columns]
        for col in missing_cols:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, col] = np.nan
        
        # Type errors (1 column)
        if 'temperature_max' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df['temperature_max'] = df['temperature_max'].astype(str)
            df.loc[mask, 'temperature_max'] = df.loc[mask, 'temperature_max'] + ' C'
        
        # Outliers (2 columns)
        if 'temperature_max' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'temperature_max'] = 600  # > 50°C
        if 'precipitation' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'precipitation'] = -abs(df.loc[mask, 'precipitation'])
        
        # Invalid values (1 type)
        if 'date' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'date'] = '1900-01-01'
    
    elif dataset_type == 'web_analytics':
        # Missing values (3 columns)
        missing_cols = [col for col in ['date_shown', 'clicked', 'converted'] if col in df.columns]
        for col in missing_cols[:3]:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, col] = np.nan
        
        # Type errors (1 column)
        if 'date_shown' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'date_shown'] = 'invalid-date-format'
        
        # Outliers (2 columns)
        if 'clicked' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'clicked'] = 2
        if 'converted' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'converted'] = 2
        
        # Invalid values (1 type)
        if 'date_shown' in df.columns:
            mask = np.random.random(n_rows) < pollution_rate
            df.loc[mask, 'date_shown'] = '1900-01-01'
    
    # Duplicates (same for all datasets)
    n_duplicates = int(n_rows * config.POLLUTION_DUPLICATE_RATE)
    if n_duplicates > 0:
        dup_rows = df.sample(n=min(n_duplicates, n_rows))
        df = pd.concat([df, dup_rows], ignore_index=True)
    
    return df
import pandas as pd
import numpy as np
from datetime import datetime

def clean_dataset(df, dataset_type):
    """Clean dataset and return cleaned DataFrame with metadata."""
    if len(df) == 0:
        return df, {}
    
    original_shape = df.shape
    original_missing = df.isnull().sum().sum()
    
    # Count pollution types in raw data
    type_errors_count = 0
    outliers_count = 0
    invalid_values_count = 0
    rows_dropped_missing_dates = 0
    
    # Count type errors and outliers before cleaning
    if dataset_type == 'bookings':
        if 'age' in df.columns:
            # Type errors: age with " years" suffix
            type_errors_count += df['age'].astype(str).str.contains('years', case=False, na=False).sum()
            # Outliers: age > 120 or < 0
            age_numeric = pd.to_numeric(df['age'].astype(str).str.replace(' years', '').str.replace('years', ''), errors='coerce')
            outliers_count += ((age_numeric < 0) | (age_numeric > 120)).sum()
        for col in ['average_daily_rate', 'revenue_available_room']:
            if col in df.columns:
                col_numeric = pd.to_numeric(df[col], errors='coerce')
                outliers_count += (col_numeric < 0).sum()
        if 'arrival_date' in df.columns and 'departure_date' in df.columns:
            arrival = pd.to_datetime(df['arrival_date'], errors='coerce')
            departure = pd.to_datetime(df['departure_date'], errors='coerce')
            # Count where departure <= arrival (invalid: should be departure > arrival)
            invalid_values_count += (departure <= arrival).sum()
    elif dataset_type == 'events':
        if 'name' in df.columns:
            type_errors_count += df['name'].astype(str).str.contains(' event', case=False, na=False).sum()
        if 'expected_attendance' in df.columns:
            outliers_count += (df['expected_attendance'] < 0).sum()
            outliers_count += (df['expected_attendance'] > 100000).sum()
        if 'date' in df.columns:
            date_parsed = pd.to_datetime(df['date'], errors='coerce')
            invalid_values_count += (date_parsed.isna() | (date_parsed < pd.Timestamp('2020-01-01'))).sum()
    elif dataset_type == 'weather':
        if 'temperature_max' in df.columns:
            type_errors_count += df['temperature_max'].astype(str).str.contains(' C', case=False, na=False).sum()
        if 'temperature_max' in df.columns:
            temp_numeric = pd.to_numeric(df['temperature_max'].astype(str).str.replace(' C', '').str.replace('C', ''), errors='coerce')
            outliers_count += (temp_numeric > 500).sum()
        if 'precipitation' in df.columns:
            outliers_count += (df['precipitation'] < 0).sum()
        if 'date' in df.columns:
            date_parsed = pd.to_datetime(df['date'], errors='coerce')
            invalid_values_count += (date_parsed.isna() | (date_parsed < pd.Timestamp('2020-01-01'))).sum()
    elif dataset_type == 'web_analytics':
        if 'date_shown' in df.columns:
            type_errors_count += (df['date_shown'] == 'invalid-date-format').sum()
        for col in ['clicked', 'converted']:
            if col in df.columns:
                outliers_count += (~df[col].isin([0, 1, np.nan])).sum()
        if 'date_shown' in df.columns:
            date_parsed = pd.to_datetime(df['date_shown'], errors='coerce')
            invalid_values_count += (date_parsed == pd.Timestamp('1900-01-01')).sum()
    
    df = df.copy()
    
    # Phase 3: Data Cleaning
    # Remove duplicates
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    
    # Fix invalid values
    if dataset_type == 'bookings':
        # Fix date issues
        if 'arrival_date' in df.columns and 'departure_date' in df.columns:
            df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')
            df['departure_date'] = pd.to_datetime(df['departure_date'], errors='coerce')
            # Fix departure < arrival
            invalid = df['departure_date'] < df['arrival_date']
            if invalid.any():
                df.loc[invalid, 'departure_date'] = df.loc[invalid, 'arrival_date'] + pd.Timedelta(days=1)
        
        # Fix negative values
        for col in ['average_daily_rate', 'revenue_available_room']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df.loc[df[col] < 0, col] = np.nan
        
        # Fix age outliers
        if 'age' in df.columns:
            df['age'] = pd.to_numeric(df['age'].astype(str).str.replace(' years', '').str.replace('years', ''), errors='coerce')
            df.loc[(df['age'] < 0) | (df['age'] > 120), 'age'] = np.nan
    
    elif dataset_type == 'events':
        # Fix type errors
        if 'name' in df.columns:
            df['name'] = df['name'].astype(str).str.replace(' event', '').str.replace('event', '')
        
        # Fix outliers
        if 'expected_attendance' in df.columns:
            df.loc[df['expected_attendance'] < 0, 'expected_attendance'] = np.nan
            df.loc[df['expected_attendance'] > 100000, 'expected_attendance'] = np.nan
        
        # Fix invalid dates
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df[df['date'] >= '2020-01-01']
    
    elif dataset_type == 'weather':
        # Fix type errors
        if 'temperature_max' in df.columns:
            df['temperature_max'] = pd.to_numeric(df['temperature_max'].astype(str).str.replace(' C', '').str.replace('C', ''), errors='coerce')
        
        # Fix outliers
        if 'precipitation' in df.columns:
            df.loc[df['precipitation'] < 0, 'precipitation'] = 0
        if 'temperature_max' in df.columns:
            df.loc[df['temperature_max'] > 500, 'temperature_max'] = np.nan
        if 'temperature_min' in df.columns:
            df.loc[df['temperature_min'] < -500, 'temperature_min'] = np.nan
        
        # Fix invalid dates
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df[df['date'] >= '2020-01-01']
    
    elif dataset_type == 'web_analytics':
        # Fix type errors and invalid dates
        if 'date_shown' in df.columns:
            df['date_shown'] = df['date_shown'].replace('invalid-date-format', np.nan)
            df['date_shown'] = pd.to_datetime(df['date_shown'], errors='coerce')
            # Drop rows with missing or invalid date_shown (including 1900-01-01)
            before_drop = len(df)
            df = df.dropna(subset=['date_shown'])
            if 'date_shown' in df.columns:
                df = df[df['date_shown'] >= '2020-01-01']
            rows_dropped_missing_dates = before_drop - len(df)
        
        # Fix outliers (invalid boolean values)
        for col in ['clicked', 'converted']:
            if col in df.columns:
                df[col] = df[col].replace(2, 0)
                df[col] = df[col].fillna(0).astype(int)
    
    if dataset_type == 'bookings':
        # Numeric imputation
        for col in ['age', 'average_daily_rate', 'revenue_available_room']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].median())
        
        # Categorical imputation
        for col in ['guest_country', 'email']:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
    
    elif dataset_type == 'events':
        for col in ['name', 'location', 'type']:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
        if 'expected_attendance' in df.columns:
            df['expected_attendance'] = df['expected_attendance'].fillna(df['expected_attendance'].median())
    
    elif dataset_type == 'weather':
        for col in ['temperature_max', 'temperature_min', 'precipitation', 'humidity']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].median())
    
    elif dataset_type == 'web_analytics':
        # Invalid dates already converted to NaT in cleaning phase above
        pass
    
    # Phase 5: Quality Metrics
    final_missing = df.isnull().sum().sum()
    completeness = 1 - (final_missing / (df.shape[0] * df.shape[1])) if df.shape[0] * df.shape[1] > 0 else 1
    
    total_rows_dropped = duplicates + rows_dropped_missing_dates
    metadata = {
        'original_shape': original_shape,
        'final_shape': df.shape,
        'duplicates_removed': duplicates,
        'rows_dropped_missing_dates': rows_dropped_missing_dates if dataset_type == 'web_analytics' else 0,
        'rows_dropped': total_rows_dropped,
        'original_missing': original_missing,
        'type_errors': type_errors_count,
        'outliers': outliers_count,
        'invalid_values': invalid_values_count,
        'final_missing': final_missing,
        'completeness': completeness
    }
    
    return df, metadata
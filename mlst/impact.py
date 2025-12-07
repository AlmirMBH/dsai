import pandas as pd
import numpy as np
import config

def measure_impact(bookings, web_analytics):
    # Data is already cleaned by data_cleaning.py, dates are already datetime
    bookings['date'] = pd.to_datetime(bookings['date'])
    recommendation_start_date = pd.to_datetime(config.RECOMMENDATION_START_DATE)
    
    conversion_rate = web_analytics['converted'].sum() / len(web_analytics)
    
    bookings_before = bookings[bookings['date'] < recommendation_start_date]
    bookings_after = bookings[bookings['date'] >= recommendation_start_date]
    
    dataset_start = pd.to_datetime(config.DATASET_START_DATE)
    dataset_end = pd.to_datetime(config.DATASET_END_DATE)
    months_before = (recommendation_start_date - dataset_start).days / 30.44
    months_after = (dataset_end - recommendation_start_date).days / 30.44
    
    equal_window_end = recommendation_start_date + pd.Timedelta(days=int(months_before * 30.44))
    bookings_after_equal = bookings_after[bookings_after['date'] < equal_window_end]
    
    np.random.seed(config.RANDOM_STATE)
    unique_guests = bookings['guest_id'].unique()
    control_group_set = set(np.random.choice(unique_guests, 
                                             size=int(len(unique_guests) * config.CONTROL_GROUP_PERCENTAGE), 
                                             replace=False))
    treatment_group = list(set(unique_guests) - control_group_set)
    control_group = list(control_group_set)
    
    treatment_after = bookings_after_equal[bookings_after_equal['guest_id'].isin(treatment_group)]
    control_after = bookings_after_equal[bookings_after_equal['guest_id'].isin(control_group)]
    
    avg_treatment_after = treatment_after['guest_id'].value_counts().reindex(treatment_group, fill_value=0).mean()
    avg_control_after = control_after['guest_id'].value_counts().reindex(control_group, fill_value=0).mean()
    
    treatment_before = bookings_before[bookings_before['guest_id'].isin(treatment_group)]
    control_before = bookings_before[bookings_before['guest_id'].isin(control_group)]
    treatment_after_full = bookings_after[bookings_after['guest_id'].isin(treatment_group)]
    control_after_full = bookings_after[bookings_after['guest_id'].isin(control_group)]
    
    avg_treatment_before = treatment_before['guest_id'].value_counts().reindex(treatment_group, fill_value=0).mean()
    avg_treatment_after_full = treatment_after_full['guest_id'].value_counts().reindex(treatment_group, fill_value=0).mean()
    avg_control_before = control_before['guest_id'].value_counts().reindex(control_group, fill_value=0).mean()
    avg_control_after_full = control_after_full['guest_id'].value_counts().reindex(control_group, fill_value=0).mean()
    
    treatment_before_rate = avg_treatment_before / months_before
    treatment_after_rate = avg_treatment_after_full / months_after
    control_before_rate = avg_control_before / months_before
    control_after_rate = avg_control_after_full / months_after
    
    ab_improvement = (avg_treatment_after - avg_control_after) / avg_control_after * 100
    did_improvement = ((treatment_after_rate - treatment_before_rate) - (control_after_rate - control_before_rate)) / treatment_before_rate * 100
    
    return {
        'conversion_rate': conversion_rate,
        'ab_test': {
            'avg_treatment': avg_treatment_after,
            'avg_control': avg_control_after,
            'improvement': ab_improvement
        },
        'did': {
            'improvement': did_improvement
        }
    }
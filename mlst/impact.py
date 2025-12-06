import pandas as pd

def measure_impact(bookings, web_analytics):
    if len(web_analytics) == 0:
        avg_without = bookings['rooms_booked'].mean()
        return {
            'conversion_rate': 0.0,
            'avg_bookings_with_recommendations': 0.0,
            'avg_bookings_without_recommendations': avg_without,
            'improvement': 0.0
        }
    
    web_analytics['date_shown'] = pd.to_datetime(web_analytics['date_shown'])
    bookings['date'] = pd.to_datetime(bookings['date'])
    
    conversion_rate = web_analytics['converted'].sum() / len(web_analytics)
    
    guests_with_recs = web_analytics['guest_id'].unique()
    bookings_with_recs = bookings[bookings['guest_id'].isin(guests_with_recs)]
    bookings_without_recs = bookings[~bookings['guest_id'].isin(guests_with_recs)]
    
    avg_bookings_with = bookings_with_recs['rooms_booked'].mean() if len(bookings_with_recs) > 0 else 0
    avg_bookings_without = bookings_without_recs['rooms_booked'].mean() if len(bookings_without_recs) > 0 else 0
    
    if avg_bookings_without > 0:
        improvement = (avg_bookings_with - avg_bookings_without) / avg_bookings_without * 100
    else:
        improvement = 0
    
    impact = {
        'conversion_rate': conversion_rate,
        'avg_bookings_with_recommendations': avg_bookings_with,
        'avg_bookings_without_recommendations': avg_bookings_without,
        'improvement': improvement
    }
    
    return impact
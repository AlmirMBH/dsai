import pandas as pd

def measure_impact(bookings, recommendations):
    if len(recommendations) == 0:
        avg_without = bookings['rooms_booked'].mean()
        return {
            'conversion_rate': 0.0,
            'avg_bookings_with_recommendations': 0.0,
            'avg_bookings_without_recommendations': avg_without,
            'improvement': 0.0
        }
    
    bookings_with_recs = bookings[bookings['date'].isin(recommendations['date'].unique())]
    bookings_without_recs = bookings[~bookings['date'].isin(recommendations['date'].unique())]
    
    conversion_rate = len(bookings_with_recs) / len(recommendations)
    
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
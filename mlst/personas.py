import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import config

def create_personas(bookings):
    guests = bookings.groupby('guest_id').agg({
        'age': 'first',
        'average_daily_rate': 'mean',
        'rooms_booked': 'sum',
        'country_id': 'first'
    }).reset_index()
    
    features = ['age', 'average_daily_rate', 'rooms_booked']
    X = guests[features].fillna(0)
    
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=config.PERSONAS_CLUSTERS, random_state=config.RANDOM_STATE)
    guests['persona_id'] = kmeans.fit_predict(x_scaled)
    
    return guests[['guest_id', 'persona_id']]


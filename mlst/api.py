from fastapi import FastAPI
from data_ingestion import get_data
from dataset_aggregation_by_day import preprocess
from forecast_prophet import train_forecast
from personas import create_personas
from recommend import recommend_events
import pandas as pd
from datetime import date
import config

app = FastAPI()

bookings, events, weather, _, bus_schedules = get_data()
if len(bookings) == 0 or len(events) == 0:
    raise FileNotFoundError("No datasets available. Please generate datasets first.")

df = preprocess(bookings, events, weather, bus_schedules)
personas = create_personas(bookings)

@app.get("/forecast/demand")
def forecast_demand(periods: int = config.DEFAULT_FORECAST_PERIODS):
    _, forecast = train_forecast(df, target='demand', periods=periods)
    return forecast[['ds', 'yhat']].tail(periods).to_dict('records')

@app.get("/forecast/revpar")
def forecast_revpar(periods: int = config.DEFAULT_FORECAST_PERIODS):
    _, forecast = train_forecast(df, target='revpar', periods=periods)
    return forecast[['ds', 'yhat']].tail(periods).to_dict('records')

@app.get("/recommend/{guest_id}")
def recommend(guest_id: int, start_date: date, end_date: date, number_of_recommendations: int = config.DEFAULT_RECOMMENDATIONS):
    recs = recommend_events(guest_id, number_of_recommendations, start_date, end_date)
    return recs[['id', 'date', 'time', 'type', 'name', 'location', 'bus_route']].to_dict('records')

@app.get("/itinerary/{guest_id}")
def get_itinerary(guest_id: int, start_date: date, end_date: date, number_of_events_per_day: int = config.DEFAULT_EVENTS_PER_DAY):
    days = (end_date - start_date).days + 1
    recs = recommend_events(guest_id, number_of_recommendations=days * number_of_events_per_day, start_date=start_date, end_date=end_date)
    
    if len(recs) == 0:
        return {"itinerary": []}
    
    recs['date'] = pd.to_datetime(recs['date'])
    recs = recs.sort_values(['date', 'time'])
    
    itinerary = []
    current_date = None
    day_plan = None
    
    for _, event in recs.iterrows():
        event_date = event['date'].date()
        
        if current_date != event_date:
            if day_plan:
                itinerary.append(day_plan)
            day_plan = {
                "day": len(itinerary) + 1,
                "date": str(event_date),
                "events": []
            }
            current_date = event_date
        
        if len(day_plan["events"]) >= number_of_events_per_day:
            continue
        
        day_plan["events"].append({
            "id": int(event['id']),
            "time": event.get('time', ''),
            "name": event['name'],
            "type": event['type'],
            "location": event['location'],
            "bus_route": event.get('bus_route', 'Walk / Taxi'),
            "expected_attendance": int(event['expected_attendance'])
        })
    
    if day_plan:
        itinerary.append(day_plan)
    
    return {"itinerary": itinerary}
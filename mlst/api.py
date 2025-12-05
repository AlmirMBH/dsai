from fastapi import FastAPI
from ingest import load_data
from preprocess import preprocess
from forecast import train_forecast
from personas import create_personas
from recommend import recommend_events
import pandas as pd
import config

app = FastAPI()

bookings, events, weather = load_data()
if len(bookings) == 0 or len(events) == 0:
    raise FileNotFoundError("No datasets available. Please generate datasets first.")

df = preprocess(bookings, events, weather)
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
def recommend(guest_id: int, n: int = config.DEFAULT_RECOMMENDATIONS):
    recs = recommend_events(guest_id, n)
    return recs[['event_id', 'date', 'type', 'name', 'location']].to_dict('records')

@app.get("/itinerary/{guest_id}")
def get_itinerary(guest_id: int, days: int = config.DEFAULT_ITINERARY_DAYS, n_per_day: int = config.DEFAULT_EVENTS_PER_DAY):
    recs = recommend_events(guest_id, n=days * n_per_day)
    
    if len(recs) == 0:
        return {"itinerary": []}
    
    recs['date'] = pd.to_datetime(recs['date'])
    recs = recs.sort_values('date')
    
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
        
        day_plan["events"].append({
            "event_id": int(event['event_id']),
            "name": event['name'],
            "type": event['type'],
            "location": event['location'],
            "expected_attendance": int(event['expected_attendance'])
        })
        
        if len(itinerary) >= days:
            break
    
    if day_plan:
        itinerary.append(day_plan)
    
    return {"itinerary": itinerary}


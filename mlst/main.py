import threading
import uvicorn
import subprocess
import sys
from ingest import load_data
from preprocess import preprocess
from forecast import train_forecast
from personas import create_personas
from recommend import recommend_events
from impact import measure_impact
import config

bookings, events, weather = load_data()
df = preprocess(bookings, events, weather)
personas = create_personas(bookings)

model_demand, forecast_demand = train_forecast(df, target='demand', periods=config.DEFAULT_FORECAST_PERIODS)
model_revpar, forecast_revpar = train_forecast(df, target='revpar', periods=config.DEFAULT_FORECAST_PERIODS)

print("Forecasts generated")
print(f"Demand forecast: {forecast_demand[['ds', 'yhat']].tail(5)}")
print(f"RevPAR forecast: {forecast_revpar[['ds', 'yhat']].tail(5)}")

recs = recommend_events(events, 1, personas, bookings, config.DEFAULT_RECOMMENDATIONS)
print(f"\nRecommendations for guest 1: {recs[['name', 'date']].head()}")

impact = measure_impact(bookings, recs)
print(f"\nImpact: {impact}")

def run_api():
    uvicorn.run("api:app", host="0.0.0.0", port=config.API_PORT, log_level="info")

def run_dashboard():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", str(config.DASHBOARD_PORT)])

print("\nStarting API server and dashboard...")
threading.Thread(target=run_api, daemon=True).start()
threading.Thread(target=run_dashboard, daemon=True).start()
print(f"API server running at http://localhost:{config.API_PORT}")
print(f"Dashboard running at http://localhost:{config.DASHBOARD_PORT}")


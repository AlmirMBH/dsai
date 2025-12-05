import threading
import uvicorn
import subprocess
import sys
from ingest import load_data
import config

bookings, events, weather = load_data()
if len(bookings) == 0 or len(events) == 0:
    print("No datasets available. Please generate datasets first.")
    exit(1)

def run_api():
    uvicorn.run("api:app", host="0.0.0.0", port=config.API_PORT, log_level="info")

def run_dashboard():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", str(config.DASHBOARD_PORT)])

print("\nStarting API server and dashboard...")
threading.Thread(target=run_api, daemon=True).start()
threading.Thread(target=run_dashboard, daemon=True).start()
print(f"API server running at http://localhost:{config.API_PORT}")
print(f"Dashboard running at http://localhost:{config.DASHBOARD_PORT}")


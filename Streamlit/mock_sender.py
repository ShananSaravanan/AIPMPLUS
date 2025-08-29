import os
import psycopg2
import requests
import random
import time
from datetime import datetime
from fastapi import FastAPI
import threading

app = FastAPI()

telemetry_url = os.getenv("telemetry_url")
db_url = os.getenv("DATABASE_URL")  # store your Render DB URL here

print(f"Using TELEMETRY_URL = {telemetry_url}")
print(f"Using DATABASE_URL = {db_url}")

# Fetch baseline stats from DB
def get_baseline_stats():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            AVG(volt), STDDEV(volt),
            AVG(rotate), STDDEV(rotate),
            AVG(pressure), STDDEV(pressure),
            AVG(vibration), STDDEV(vibration)
        FROM telemetry;
    """)
    row = cur.fetchone()
    conn.close()
    return {
        "volt": (row[0], row[1]),
        "rotate": (row[2], row[3]),
        "pressure": (row[4], row[5]),
        "vibration": (row[6], row[7]),
    }

stats = get_baseline_stats()
print("Baseline stats:", stats)

def send_loop():
    machine_ids = list(range(1, 101))
    while True:
        for machine_id in machine_ids:
            data = {
                "machineid": machine_id,
                "datetime": datetime.now().isoformat(),
                "volt": random.gauss(stats["volt"][0], stats["volt"][1]),
                "rotate": random.gauss(stats["rotate"][0], stats["rotate"][1]),
                "pressure": random.gauss(stats["pressure"][0], stats["pressure"][1]),
                "vibration": random.gauss(stats["vibration"][0], stats["vibration"][1]),
            }
            try:
                response = requests.post(telemetry_url, json=data)
                print(f"[{machine_id}] Status {response.status_code}")
            except Exception as e:
                print(f"[{machine_id}] Failed: {e}")
        time.sleep(5)

# Start loop in background thread
threading.Thread(target=send_loop, daemon=True).start()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

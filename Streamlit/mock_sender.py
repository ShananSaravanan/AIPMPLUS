# # mock_sender.py
# import requests
# import random
# import time
# from datetime import datetime
# import os
# # Machine IDs to simulate
# machine_ids = list(range(1, 101))  # includes 1 to 100
# telemetry_url = os.environ.get("telemetry_url")   
# while True:
#     for machine_id in machine_ids:
#         data = {
#             "machineid": machine_id,
#             "datetime": datetime.now().isoformat(),
#             "volt": random.uniform(97.333603782359, 255.124717259791),
#             "rotate": random.uniform(138.432075304341, 695.020984403396),
#             "pressure": random.uniform(51.2371057734253, 185.951997730866),
#             "vibration": random.uniform(14.877053998383, 76.7910723016723)
#         }

#         try:
#             response = requests.post(telemetry_url, json=data)
#             if response.status_code == 200:
#                 print(f"[{machine_id}] ✅ Sent: {data['datetime']} | Status: {response.status_code}")
#             else:
#                 print(f"[{machine_id}] ❌ Failed: {response.status_code} - {response.text}")
#         except Exception as e:
#             print(f"[{machine_id}] ❌ Failed to send: {e}")

#     time.sleep(5)  # Send every 5 seconds

import os
import requests
import random
import time
from datetime import datetime
from fastapi import FastAPI
import threading

app = FastAPI()

telemetry_url = os.getenv("telemetry_url")

def send_loop():
    machine_ids = list(range(1, 101))
    while True:
        for machine_id in machine_ids:
            data = {
                "machineid": machine_id,
                "datetime": datetime.now().isoformat(),
                "volt": random.uniform(97.3, 255.1),
                "rotate": random.uniform(138.4, 695.0),
                "pressure": random.uniform(51.2, 185.9),
                "vibration": random.uniform(14.8, 76.7)
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

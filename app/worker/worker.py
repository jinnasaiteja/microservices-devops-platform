import time
import os

WORKER_NAME = os.getenv("WORKER_NAME", "default-worker")

def process_jobs():
    while True:
        print(f"[{WORKER_NAME}] checking for jobs...")
        time.sleep(10)
        print(f"[{WORKER_NAME}] no pending jobs found")
        time.sleep(5)

if __name__ == "__main__":
    print(f"Starting worker: {WORKER_NAME}")
    process_jobs()

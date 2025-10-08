import json
import redis
from celery.schedules import crontab

# --- Configuration ---
# This key is where the redisbeat scheduler finds its schedule
SCHEDULER_KEY = 'redisbeat:schedule'
# Connect to the Redis instance defined in your Celery config
REDIS_URL = 'redis://localhost:6379/1'
# --- End Configuration ---

def add_task_to_schedule():
    """
    Connects to Redis and adds the periodic task definition.
    """
    print("Connecting to Redis...")
    redis_conn = redis.from_url(REDIS_URL, decode_responses=True)

    task = {
        'name': 'process-retry-folder-every-5-minutes',
        'task': 'celery_masterapp.process_retry_folder',
        # You can use seconds (300) or a crontab dictionary
        'schedule': {'minute': '*/5', 'hour': '*', 'day_of_week': '*'},
        'args': [],
        'kwargs': {},
        'enabled': True
    }

    print(f"Adding task '{task['name']}' to Redis schedule...")
    
    # The score of 0 means it will run on the next available slot
    # The member is the JSON-encoded task definition
    redis_conn.zadd(SCHEDULER_KEY, {json.dumps(task): 0})
    
    print("Task added successfully.")

if __name__ == "__main__":
    add_task_to_schedule()
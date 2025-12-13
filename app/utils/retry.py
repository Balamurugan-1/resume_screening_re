import time
import random

def retry_llm(fn, retries=3, base_delay=1):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if attempt == retries - 1:
                raise e
            sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(sleep_time)

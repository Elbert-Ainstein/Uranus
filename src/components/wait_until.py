from typing import Callable
from timeit import default_timer as timer
import time

## A small timeout & adds condition to get sensor working first 
def wait_until(condition: Callable[[], bool], timeout: float = 5, poll_delay: float = 0.01):
    start_time = timer()
    while timer() - start_time < timeout:
        if condition():
            return True
        time.sleep(poll_delay)
    if not condition():
        return False   
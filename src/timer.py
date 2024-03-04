
import time

class Timer:
    def __init__(self):    
        self.elapsed_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed_time = time.time() - self.start_time

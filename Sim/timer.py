# timer.py

import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None
        self.elapsed_time = 0
        self.pauseTime = 0

    def set_default(self):
        self._start_time = None
        self.elapsed_time = 0
        self.pauseTime = 0

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()
        self.pauseTime = 0
        self.elapsed_time = 0

    def state(self):
        """Chcek state"""
        if self._start_time is not None:
            return True
        else:
            return False

    def pause(self, pause_Timer):
        self.pauseTime = pause_Timer

    def read_time(self):
        if self._start_time is not None:
            self.elapsed_time = round(time.perf_counter() - self._start_time - self.pauseTime, 1)
            #print(f"Elapsed time: {self.elapsed_time} seconds")
            return self.elapsed_time
        else:
            self.elapsed_time = 0
            return self.elapsed_time

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        self.elapsed_time = round(time.perf_counter() - self._start_time - self.pauseTime, 1)

        self._start_time = None
        print(f"Elapsed time: {self.elapsed_time} seconds")

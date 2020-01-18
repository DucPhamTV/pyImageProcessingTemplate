# A simple timer by python threading

import threading
import time
import logging

from logger import create_stream_handler

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)


class Timer(threading.Thread):
    def __init__(self, interval, callback, timeout=10, drift=True, *args, **kwargs):
        super().__init__()
        self.stop_flag = threading.Event()
        self.interval = interval
        self.callback = callback
        self.drift = drift
        self.timeout = timeout
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stop_flag.set()
        self.join(self.timeout)

    def run(self):
        log.info("interval {}".format(self.interval))
        next_period = self.interval
        next_time = time.time()
        error_counter = 0

        while not self.stop_flag.wait(next_period):
            self.callback(*self.args, **self.kwargs)
            if not self.drift and self.interval > 0:
                next_time += self.interval
                next_period = next_time - time.time()
                log.info(f"next_time {next_time}, next_period {next_period}")
                if next_period < 0:
                    error_counter += 1
                    while next_time < time.time():
                        next_time += self.interval
                    if error_counter > 5:  # after 5 times later than interval. We stop it
                        log.error("Execution time is larger than interval, stopping timer")
                        break
                else:
                    error_counter = 0 # reset error_counter


# A simple timer by python threading

import threading
import time


class Timer(threading.Thread):
    def __init__(self, interval, callback, timeout=10, driff=True, *args, **kargs):
        super().__init__(self)
        self.stop = Event()
        self.interval = interval
        self.callback = callback
        self.drift = drift
		self.timeout = timeout
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stop.set()
        self.join(self.timeout)

    def run(self):
        next_period = self.interval
        next_time = time.time()

        while not self.stop.wait(next_period):
            self.callback(*self.args, **self.kwargs)
            next_time += self.interval
            next_period = next_time - time()
			if next_period < 0:
				log.error("Execution time is larger than interval, stopping timer")
				break


# Control fps of a camera
import logging
import time
import threading
import queue
import sys

#from collections import deque

import cv2

from logger import create_file_handler, create_stream_handler
from common.Timer import Timer

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)


class FPS_Controller(object):
    def __init__(self, fps=0):
        self.fps = fps # 0 means read max fps
        self.is_running = None
        self.cap = cv2.VideoCapture(0)
        self.buffer = queue.Queue(10)
        if fps == 0:
            self.frame_reader = Timer(
                interval=0, callback=self.read_frames, drift=True)
        else:
            self.frame_reader = Timer(
                interval=1.0 / fps, callback=self.read_frames, drift=False)


    def read_frames(self):
        ret, frame = self.cap.read()
        log.info("read a frame")
        try:
            self.buffer.put_nowait(frame)
        except queue.Full:
            log.warning("Buffer is full, eject oldest frame")
            self.buffer.get_nowait()
            self.buffer.put_nowait(frame)

    def start(self):
        self.is_running = True
        self.frame_reader.start()
        # Wait a while for frames are filled to buffer
        time.sleep(0.5)
        while self.is_running:
            frame = self.buffer.get()
            log.info("yielding a frame")
            yield frame

    def stop(self):
        self.frame_reader.stop()
        self.cap.release()
        self.is_running = False
        log.info("Released")


if __name__ == "__main__":
    fps = sys.argv[1]
    start = time.time()
    frame_counter = 0
    controller = FPS_Controller(int(fps))
    for frame in controller.start():
        cv2.imshow('frame', frame)
        frame_counter += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            controller.stop()
    stop = time.time()
    elapsed = stop - start
    log.info("Read {} frames in {} seconds. FPS: {}".format(
        frame_counter, elapsed, frame_counter / elapsed))

    cv2.destroyAllWindows()

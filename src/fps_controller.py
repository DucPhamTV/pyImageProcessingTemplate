# Control fps of a camera
import logging
import time
import threading

from collections import deque

import cv2

from logger import create_file_handler, create_stream_handler
from common.Timer import Timer

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)


class FPS_Controller(object):
    def __init__(self, fps=0):
        self.fps = fps # 0 means read max fps
        self.cap = cv2.VideoCapture(0)
        self.frame = deque([], )
        if fps == 0:
            self.frame_reader = Timer(
                interval=0, callback=read_frames, drift=True)
        else:
            self.frame_reader = Timer(
                interval=1.0 / fps, callback=read_frames, drift=False)


    def read_frames():
        cap = cv2.VideoCapture(0)
        cap.release()


if __name__ == "__main__":
    start = time.time()
    log.debug("Start capturing frame in separate thread")
    cap_thread = threading.Thread(target=reading_frames)
    cap_thread.start()
    log.debug("Sleeping in main thread")
    for i in range(60):
        time.sleep(1)
        log.debug(i)

    cap_thread.join()
    stop = time.time()
    log.debug("elapsed time %d" % (stop - start))


cv2.destroyAllWindows()

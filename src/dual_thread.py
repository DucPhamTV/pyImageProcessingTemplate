import logging
import time
import threading
import queue

import cv2
import numpy as np
import matplotlib.pyplot as plt

from logger import create_file_handler, create_stream_handler
from fps_controller import FPS_Controller

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)

haar_cascade_face = cv2.CascadeClassifier('lib/face_detection/haarcascade_frontalface_default.xml')

def image_processing(buff, event):
    # Simulating heavy CPU work load
    while not event.is_set():
        frame = buff.get()
        log.info("In Thread: got an image")
        f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for _ in range(10):
            faces_rects = haar_cascade_face.detectMultiScale(f_gray, scaleFactor = 1.2, minNeighbors = 5)
        for (x,y,w,h) in faces_rects:
             cv2.rectangle(f_gray, (x, y), (x+w, y+h), (0, 255, 0), 2)


class FrameBuffer(object):
    def __init__(self, max_buffer=10):
        self.queue = queue.Queue(max_buffer)

    def put(self, frame):
        try:
            self.queue.put_nowait(frame)
        except queue.Full:
            log.warning("Full buffer, pop the oldest frame out")
            self.queue.get_nowait()  # Pop the oldest frame to push the latest
            self.queue.put_nowait(frame)

    def get(self):
        return self.queue.get()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    n = 0
    start = time.time()

    log.info("Starting")
    fb = FrameBuffer()
    event = threading.Event()
    process_thread = threading.Thread(
        target=image_processing, name='processing', args=(fb, event))
    process_thread.start()

    while True:
        log.info("Read image")
        ret, frame = cap.read()
        fb.put(frame)
        n += 1
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            event.set()
            break

    stop = time.time()
    log.info("FPS: %d" % (n / (stop - start)))
    process_thread.join()
    cap.release()
    cv2.destroyAllWindows()

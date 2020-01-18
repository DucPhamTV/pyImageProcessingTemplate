import logging
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt

from logger import create_file_handler, create_stream_handler
from fps_controller import FPS_Controller

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)

haar_cascade_face = cv2.CascadeClassifier('lib/face_detection/haarcascade_frontalface_default.xml')

def image_processing(frame):
    # Simulating heavy CPU work load
    f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for _ in range(10):
        faces_rects = haar_cascade_face.detectMultiScale(f_gray, scaleFactor = 1.2, minNeighbors = 5)
    for (x,y,w,h) in faces_rects:
         cv2.rectangle(f_gray, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return f_gray

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    n = 0
    start = time.time()
    log.info("Starting")
    while True:
        log.info("Read image")
        ret, frame = cap.read()
        n += 1
        log.info("Processing")
        result = image_processing(frame)
        log.info("Process Done")
        cv2.imshow('frame', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stop = time.time()
    log.info("FPS: %d" % (n / (stop - start)))
    cap.release()
    cv2.destroyAllWindows()

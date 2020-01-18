# This one is for testing the maximun fps of a camera. The loop reads frame nonstop
import logging
import time

import cv2

from logger import create_file_handler, create_stream_handler

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    n = 0
    start = time.time()
    while (True):
        ret, frame = cap.read()
        assert ret
        n += 1
        cv2.imshow('aaa', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stop = time.time()
    delta = stop - start
    cap.release()
    log.info("elapsed time: %d, FPS %d" % (delta, n / delta))
    cv2.destroyAllWindows()



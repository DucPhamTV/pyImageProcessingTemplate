import logging
import time
import cv2

from logger import create_file_handler, create_stream_handler

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    start = time.time()
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q') or n > 100:
            break
    stop = time.time()
    cap.release()
    log.debug("elaspsed after 100 frames: %d" % (stop - start))

cv2.destroyAllWindows()

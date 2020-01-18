import logging
import time
import cv2

from logger import create_file_handler, create_stream_handler
from fps_controller import FPS_Controller

log = logging.getLogger(__name__)
log.addHandler(create_stream_handler())
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    start = time.time()
    controller = FPS_Controller()
    for frame in controller.start():
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray,(5,5),0)
        # Add your image processing works here.
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            controller.stop()

    cv2.destroyAllWindows()

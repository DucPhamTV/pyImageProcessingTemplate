# pyImageProcessingTemplate
Simple project using OpenCV + python, How to optimize output streaming and performance

### set up environment

make venv
source venv/bin/activate

### Run single thread code. the frames aren't really smooth. Notice the FPS at the end.
python src/single_thread.py

### Run dual thread code. The frames are better because of higher FPS
python src/dual_thread.py

### Calculate FPS of a camera
python src/fps_measurement.py

### Read frames on a camera with particular FPS. E.g 7 frames per second
python src/fps_controller.py 7

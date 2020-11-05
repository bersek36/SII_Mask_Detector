import cv2
import imutils

class Camera(object):
    def __init__(self):
        
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    
    def get_frame(self):

        success, frame = self.video.read()
        frame = imutils.resize(frame, width=400)
        return success, frame

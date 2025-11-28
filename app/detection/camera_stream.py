import cv2

class CameraStream:

    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.capture = None

    def connect(self):
        self.capture = cv2.VideoCapture(self.rtsp_url)

    def get_frame(self):
        if not self.capture:
            self.connect()

        ret, frame = self.capture.read()
        if ret:
            return frame
        return None

    def release(self):
        if self.capture:
            self.capture.release()

import cv2
from  picamera.array import PiRGBArray
from picamera import PiCamera
import time
import io
import threading

#video = None


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.size = (160, 120)
        self.fps = 8
        self.video = PiCamera()
        self.video.resolution = self.size
        self.video.framerate = self.fps
        self.rawCapture = PiRGBArray(self.video, size=self.size)
        self.imgIndex = 0
        self.time = time.time()
        self.threads = []
        self.outputpath = '/home/pi/opencv/rpcar/cameraimages'
        #video = self
        time.sleep(0.1)
        t = threading.Thread(target=self.doCamera, args=(self,))
        self.threads.append(t)
        t.start()
        time.sleep(1)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        #self.image = self.getFrame()

    def getFrame(self):
        stream = io.BytesIO()
        for frame in self.video.capture_continuous(self.rawCapture, format='bgr', use_video_port=True):
            image = frame.array
            return image
        return None
        	
    def doCamera(self,video):
        for frame in self.video.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            video.image = image
            video.rawCapture.truncate(0)
            video.image = cv2.cvtColor(video.image,cv2.COLOR_BGR2GRAY)
            ret, jpeg = cv2.imencode('.jpg',video.image)
            self.bytes = jpeg.tobytes()
            #print('new frame')
            #print("update image")

    def __del__(self):
        #self.video.release()
        self.video.close()
    
    def get_frame(self):
        #success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        #self.image = self.getFrame()
        #self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #ret, jpeg = cv2.imencode('.jpg', self.image)
        #self.bytes = jpeg.tobytes()
        curTime = time.time()
        if curTime-self.time>=1:           
           self.time = curTime 
           cv2.imwrite(self.outputpath + '/' + str(curTime)+'.jpg', self.image)
        return self.bytes
        #return self.image

        #for frame in self.video.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
        #    image = frame.array
        #    ret, jpeg = cv2.imencode('.jpg', image)
        #    return jpeg.tobytes()
        #return None

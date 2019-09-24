import cv2
from base_camera import BaseCamera
import time




# Must be set from server
main = lambda :0

class Camera(BaseCamera):
    @staticmethod
    def frames():
        while True:
            # read current frame
            # if main.VideoSettings.cameraNeedsChange:
            #         camera = cv2.VideoCapture(main.VideoSettings.selectedCamera)
            #         res = main.VideoSettings.resolution
            #         if res[0] > 0:
            #             camera.set(3, main.VideoSettings.resolution[0])
            #             camera.set(4, main.VideoSettings.resolution[1])
            #         main.VideoSettings.cameraNeedsChange = False
            
            result = main()
            
            # Put update loop here
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', result)[1].tobytes()

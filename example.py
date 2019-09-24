from server import create_server
import numpy as np
from framecapture import WebcamCapture,Recorded

frameCapture = WebcamCapture()

class ExampleClass():
    def __init__(self):
        self.single_value = np.random.random()
        self.array = np.random.random(30)
        self.multiplier = 1
        self.x = np.arange(30)
    def update(self):
        self.single_value= np.random.random() * self.multiplier
        self.array = np.random.random(30) * self.multiplier
 

Example = ExampleClass()
def main():        
    frame = frameCapture.get_frame()
    Example.update()
    return frame
        





            #host="0.0.0.0"

if __name__ == '__main__':
    app = create_server([Example],main,"/home/martin/repos/myclient",True)
    app.run(threaded = True)


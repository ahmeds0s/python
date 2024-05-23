import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import numpy as np
import serial
import time
from os import environ




environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR "] = "1"
environ["QT_SCREEN_SCALE_FACTORS "] = "1"
environ["QT_SCALE_FACTOR"] = "1"

img = image.imread("./foot.jpg")


class animator:
    def __init__(self, img):
        print("initialization....")
        self.img = img
        self.ser = None
        self.sensors_locations = np.array([
                    (150, 70),
                    (113, 290),
                    (180, 580),
                    (347, 573),
                    (309, 700),
                    (123, 857)
                ])
        while True:
            try:
                self.ser = serial.Serial("COM5", 9600, timeout=1) 
            except Exception as e:
                print(e)

            finally:
                if self.ser !=  None:
                    time.sleep(1)
                    print("connected to  ", self.ser.portstr)
                    break
        self.readings = []
    

    def animate(self, i):
        print("animate")
        print(self.readings)
        self.read_from_arduino()
        if not self.is_ready():
            return
        
        plt.clf()
        plt.axis("off")
        plt.imshow(img)
        grads = np.linspace(0, 1, 7)
        for i, loc in enumerate(self.sensors_locations):
            plt.scatter(loc[0] * np.ones(7), (loc[1] * np.ones(7)),alpha = (1 - grads), s = 2000 * grads * self.readings[i], cmap="Reds", c=(1 - grads) * 1000) 
        plt.show()


    def start_animation(self):
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect("close_event", self.end_animation)
        self.anim = FuncAnimation(self.fig, self.animate, frames=50, interval=50)
        ax_button = plt.axes([1, 1, 1, 1])
        self.button = Button(ax_button, "Stop")
        self.button.on_clicked(self.button_event)
        plt.show()
        print("done")
    

    def read_from_arduino(self):
        print("reading......")
        self.readings = []
        for _ in range(6):
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').rstrip()
                    self.readings.append(float(line))

            # time.sleep(0.1)
            
            except Exception as e:
                print(e)
                self.ser.close()
    def is_ready(self):
        if len(self.readings) > 6:
            self.readings = self.readings[-(len(self.readings) % 6):]
            return False 
        elif len(self.readings) < 6:
            return False
        else:
            return True

    def end_animation(self, event):
        try:
            self.ser.close()
        except Exception as e:
            print(e)

    def button_event(event):
        print("button clicked")
        
        


a = animator(img)
a.start_animation()


        


import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import  Button
from matplotlib.gridspec import GridSpec as gridspec
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
        self.readings = []
        self.fig = plt.figure() 
        self.grid = gridspec(2, 3)

    def animate(self, i):
        print("animate")
        print(self.readings)
        self.read_from_arduino()
        if not self.is_ready():
            return
        
        self.ax1.clear()
        self.ax1.axis("off")
        self.ax1.imshow(img)
        grads = np.linspace(0, 1, 7)
        for i, loc in enumerate(self.sensors_locations):
            plt.scatter(loc[0] * np.ones(7), (loc[1] * np.ones(7)),alpha = (1 - grads), s = 2000 * grads * self.readings[i], cmap="Reds", c=(1 - grads) * 1000) 
        plt.draw()


    def start_animation(self, event):
        # start serial 
        self.start_serial()
        # clearing the start event 
        self.bt.ax.remove()
        self.bt.disconnect_events()
        # connect figure closing event to close the serial port before ending
        self.fig.clear()
        self.fig.canvas.mpl_connect("close_event", self.end_animation)
        

        # create the grids of the interface of the app
        self.ax1 = self.fig.add_subplot(self.grid[0, :])
        self.end_ax = self.fig.add_subplot(self.grid[1, 0])
        self.end_ax.set_position([0.1, 0.1, 0.1, 0.1])
        

        self.end_bt = Button(self.end_ax, "END")
        self.end_bt.on_clicked(self.button_event)
        self.text1_ax = self.fig.add_subplot(self.grid[1, 1])
        self.text2_ax = self.fig.add_subplot(self.grid[1, 2])
        

        self.text2_ax.axis('off')
        self.text1_ax.axis('off')

        

        self.text1_ax.text(0.1, 0.1, "text1",
        fontsize=14, color='green', ha='right', va='top', 
        bbox=dict(facecolor='red', alpha=0.5))



        self.text2_ax.text(0.1, 0.1, "text2",
        fontsize=14, color='red',  va='top', 
        bbox=dict(facecolor='yellow', alpha=0.5))
      


        
        self.anim = FuncAnimation(self.fig, self.animate, frames=100, interval=50)
        plt.draw()
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

    def button_event(self, event):
        print("button clicked")
    

    def before_start(self):
        self.start_button = self.fig.add_subplot(self.grid[:, :])
        self.start_button.set_position([0.4, 0.4, 0.2, 0.1]) # [left, bottom, width, height]
        self.bt = Button(self.start_button, "start")
        self.start_event = self.bt.on_clicked(self.start_animation)
        plt.show()

    def start_serial(self):
     
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
    def temp_animate(self, i):
        self.ax1.clear()
        self.ax1.imshow(img)
        self.ax1.axis("off")
        self.ax1.scatter(x, 100 * np.sin(x - i * 0.1))
        plt.draw()

        
x = np.linspace(0, 100, 1000)       
 
        

        
        


a = animator(img)
a.before_start()


        


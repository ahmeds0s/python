import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.gridspec import GridSpec as gridspec
import numpy as np
import serial
import time
from os import environ

com = "COM3"


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
        self.grid = gridspec(2, 3, height_ratios=[4, 1])

    def animate(self, i):
        print("animate")
        print(self.readings)
        self.read_from_arduino()
        if not self.is_ready() or not self.start:
            return
        self.update_text()
        self.ax1.clear()
        self.ax1.axis("off")
        self.ax1.imshow(img, aspect="equal")
        grads = np.linspace(0, 1, 7)
        if sum(self.readings) != 0:
            self.calculate_center_of_pressure()
            self.ax1.scatter(self.cop[0], self.cop[1], c="r.")

        for i, loc in enumerate(self.sensors_locations):
            self.ax1.scatter(loc[0] * np.ones(7), (loc[1] * np.ones(7)), alpha=(1 - grads), s=500 * grads * self.readings[i], cmap="Reds", c=(1 - grads) * 1000)
        plt.draw()

    def start_animation(self, event):
        self.start = True
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
        self.text_ax = self.fig.add_subplot(self.grid[1, 1:])
        self.text1 = self.text_ax.text(0.4, 0.5, "Text 1", fontsize=12)
        self.text2 = self.text_ax.text(0.7, 0.5, "text 2", fontsize=12)

        self.text_ax.axis('off')

        self.anim = FuncAnimation(
            self.fig, self.animate, frames=100, interval=1)
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
        self.start = False
        try:
            self.ser.close()
        except Exception as e:
            print(e)

    def button_event(self, event):
        print("button clicked")

    def before_start(self):
        self.start_button = self.fig.add_subplot(self.grid[:, :])
        # [left, bottom, width, height]
        self.start_button.set_position([0.4, 0.4, 0.2, 0.1])
        self.bt = Button(self.start_button, "start")
        self.start_event = self.bt.on_clicked(self.start_animation)
        plt.show()

    def start_serial(self):

        while True:
            try:
                self.ser = serial.Serial(com, 9600, timeout=1)
            except Exception as e:
                print(e)

            finally:
                if self.ser != None:
                    time.sleep(1)
                    print("connected to  ", self.ser.portstr)
                    break

    def temp_animate(self, i):
        print("animate")
        self.ax1.clear()
        self.ax1.axis("off")
        self.ax1.imshow(img)
        grads = np.linspace(0, 1, 7)
        for i, loc in enumerate(self.sensors_locations):
            self.ax1.scatter(loc[0] * np.ones(7), (loc[1] * np.ones(7)), alpha=(1 - grads),
                             s=2000 * grads * np.random.randint(0.5, 1), cmap="Reds", c=(1 - grads) * 1000)
        plt.draw()

    def calculate_center_of_pressure(self):
        if sum(self.readings) == 0:
            self.cop = np.array([0, 0])
            return
        sum_pressure = np.array([0, 0])
        for i in range(0, 2):
            for index, loc in enumerate(self.sensors_locations):
                sum_pressure[i] += loc[i] * self.readings[index]
        self.cop = sum_pressure / np.sum(self.readings)
    def update_text(self):
        if self.readings[2] > 4:
            self.text1.set_text("Flat Foot")
        for r in self.readings:
            if r > 5:
                self.text1.set_text("Over Pressure")
        


x = np.linspace(0, 100, 1000)


a = animator(img)
a.before_start()

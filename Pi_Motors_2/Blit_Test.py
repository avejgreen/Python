import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import sys, time

fig, ax = plt.subplots()
line, = ax.plot(np.random.rand(10))

def f0():

    ax.set_ylim(0, 1)
    return line

def update(data):
    line.set_ydata(data)
    return line,

def data_gen():
    # while True:
    yield np.random.rand(10)
    test = 1

ani = FuncAnimation(fig, update, data_gen, init_func=f0, blit=True, interval=10)
plt.show()


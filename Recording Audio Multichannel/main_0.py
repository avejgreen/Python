# import pyaudio
import wave
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

cmap = plt.get_cmap('plasma')
thing_exact = 255/12
new_cmap = []

for i in range(13):

    j = int(np.round(thing_exact * i))
    new_cmap.append(np.round(255 * np.array(cmap.colors[j])))

test = 1
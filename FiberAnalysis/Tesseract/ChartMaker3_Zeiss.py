import importlib.util
import subprocess
import sys

packages_required = ['numpy', 'matplotlib', 'glob', 'csv', 're', 'tkinter', 'pytesseract', 'PIL', 'os']

for package in packages_required:
    spec = importlib.util.find_spec(package)
    if spec is None:
        print('Installing package ' + package + '... ')
        subprocess.call([sys.executable, "-m", "pip", "install", package])
        print('Done!')
    test = 1

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import glob, csv, re
import tkinter as tk
from tkinter import filedialog
import pytesseract
from PIL import Image
import os


#####################
## Latest update: 180713
## REMOVED TESSERACT in favor of jpg xml reads
##
## Modus operandi:
## 1. Use tkinter to locate histograms, original images
## 2. For each file, gather the data in an array, scale to image magnification
##      a. Open original SEM image, crop it, and extract the magnification
##      b. Get data from the original histogram CSV, scale and save new data
##      c. Create new scaled histogram plot and save it.
## 3. Create new histogram data and plot for aggregated data.
#####################


## 1. Use tkinter to locate histograms, original images
root = tk.Tk()
root.withdraw()

np.set_printoptions(precision=3)

# test_path = '/Users/averygreen/Documents/Viaex/SEM/180616/1024/Best Segmentation/Histograms'
old_hist_path = filedialog.askdirectory(title='Choose histogram directory',
                                        initialdir='/Users/averygreen/Documents/Viaex/SEM',
                                        parent=root)
new_hist_path = old_hist_path + '/Scaled'
try:
    os.mkdir(new_hist_path)
except FileExistsError:
    pass

orig_img_path = filedialog.askdirectory(title='Choose original SEM image directory',
                                        initialdir='/'.join(re.split('/', old_hist_path)[0:-2]),
                                        parent=root)

old_hist_filenames = glob.glob(old_hist_path + '/*Radius Histo.csv')
old_hist_filenames.sort()
all_data = []
file_number = -1

# Phenom and Zeiss have different scale locations.
# Have boolean to indicate Phenom or Zeiss. True indicates Phenom.
phenom_or_zeiss = False

def read_um_per_pix(image):
    xml_string = str(image.applist[2][1])
    pixel_height_start_idex = re.search('pixelHeight unit', xml_string).regs[0][0]
    return float(re.search('>\d+[.]\d+<', xml_string[pixel_height_start_idex:]).group(0)[1:-1])

def measure_um_per_pix(image):

    if phenom_or_zeiss:
        mag_bbox = np.array([378, 1029, 478, 1054]) * image.size[0] / 1024
    else:
        mag_bbox = np.array([1420, 1400, 1630, 1460]) * image.size[0] / 2048
    mag_bbox = tuple(mag_bbox.astype(int))
    mag_image = image.crop(mag_bbox)

    if phenom_or_zeiss:
        def lut_fcn(input_pt):
            if input_pt < 64:
                return 0
            else:
                return 255
        mag_image = mag_image.point(lut_fcn)

        mag_text_readout = pytesseract.image_to_string(mag_image)
        mag_text = re.sub(' ', '', mag_text_readout)
        mag_text = re.sub('Z', '2', mag_text)
        mag_text = re.sub('B', '8', mag_text)
        mag_text = re.sub('S', '5', mag_text)
        mag_text = re.sub('O', '0', mag_text)
        mag_text = re.sub('D', '0', mag_text)
        mag_text_split = re.search('[a-zA-Z]+', mag_text).start()

        mag_text = [mag_text[:mag_text_split], mag_text[mag_text_split:]]
        mag_value = float(mag_text[0])
        mag_scaler = (10 / 205) * 5400

    else:
        mag_text_readout = pytesseract.image_to_string(mag_image)
        mag_text_split = re.search('[a-zA-Z]+', mag_text_readout).start()
        mag_text = [mag_text_readout[:mag_text_split], mag_text_readout[mag_text_split:]]
        mag_value = float(mag_text[0])
        if 'K' in mag_text[1]:
            mag_value *= pow(10, 3)
        elif 'M' in mag_text[1]:
            mag_value *= pow(10, 6)
        mag_scaler = (1 / 105) * 11720

    # Use mag scaler to calibrate image scales
    # Comes from M = 5400x image that has 10 um / 205 pix
    # Divide mag_scaler by M_new to get new pixel scaling.
    try:
        return mag_scaler / mag_value
    except:
        test = 1

## 2. For each file, gather the data in an array, scale to image magnification
for new_full_filename in old_hist_filenames:

    file_number += 1

    ## a. Open original SEM image, crop it, and extract the magnification
    pic_name = '_'.join(re.split('_', re.split('/', new_full_filename)[-1])[:-2])
    new_image = Image.open(glob.glob(orig_img_path + '/' + pic_name + '.*')[0])
    um_per_pix = measure_um_per_pix(new_image)

    ## b. Get data from the original histogram CSV, scale and save new data

    reader = csv.reader(open(new_full_filename))
    csv_data = np.array(list(reader))

    diameters = 2 * np.array(csv_data[1:, 0], dtype=float)
    freqs = np.array(csv_data[1:, 1], dtype=float)
    freqs = freqs/sum(freqs)

    last_datapt_index = max(np.nonzero(freqs)[0])
    diameters = diameters[:last_datapt_index]
    freqs = freqs[:last_datapt_index]

    # diameters = diameters * pix_to_um
    diameters = diameters * um_per_pix

    csv_file = open(new_hist_path + '/' + pic_name + '.csv', 'w+')
    csv_writer = csv.writer(csv_file)
    csv_output = np.array([freqs, diameters])
    csv_output = np.transpose(csv_output)
    csv_output = np.around(csv_output, decimals=3)
    csv_writer.writerow(['Frequency', 'Diameter'])
    csv_writer.writerow(['norm', 'um'])
    csv_writer.writerows(csv_output)
    csv_file.close()

    all_data.append([diameters, freqs, pic_name])


    ## c. Create new scaled histogram plot and save it.
    axes = plt.gca()
    axes.fill_between(diameters, 0, freqs)
    axes.set_xlabel('Fiber Diameter (um)')
    axes.set_ylabel('Frequency (norm)')
    # plt.hist(freqs, diameters)

    plt.savefig(new_hist_path + '/' + pic_name + '.png', dpi=144)

    plt.cla()

    print('Finished ' + pic_name)


## 3. Create new histogram data and plot for aggregated data.
for histdata in all_data:

    axes = plt.gca()
    axes.plot(histdata[0], histdata[1], label=histdata[2])
    axes.set_xlabel('Fiber Diameter (um)')
    axes.set_ylabel('Frequency (norm)')
    axes.legend()

plt.savefig(new_hist_path + '/All_Data.png', dpi=144)

plt.cla()

plt.close(plt.gcf())

test = 1

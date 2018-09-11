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
# TO DO:
# Delete the cropped mag text image
#####################


root = tk.Tk()
root.withdraw()

np.set_printoptions(precision=3)

# Path = '/Users/averygreen/Documents/Viaex/SEM/180616/1024/Best Segmentation/Histograms'
Path = filedialog.askdirectory(title='Choose histogram directory',
                               initialdir='/Users/averygreen/Documents/Viaex/SEM',
                               parent=root)

NewPath = Path + '/AG_Data'
try:
    os.mkdir(NewPath)
except FileExistsError:
    pass

HistFileNames = glob.glob(Path + '/*Radius Histo.csv')
HistFileNames.sort()
AllData = []

for NewFileName in HistFileNames:
    label = ''.join(re.split('_', re.split('/', NewFileName)[-1])[:-2])
    if label == 'Training0002':
        test = 1
    reader = csv.reader(open(NewFileName))
    csv_data = np.array(list(reader))

    start_pic_name = [x.start() for x in re.finditer('/', NewFileName)][-1] + 1
    end_pic_name = [x.start() for x in re.finditer('_', NewFileName)][-2]
    pic_name = NewFileName[start_pic_name:end_pic_name]
    img_path_end = re.search('Best Segmentation', Path).span()[0] - 1
    img_path = Path[:img_path_end]
    # img_path = filedialog.askdirectory(title='Choose original image directory',
    #                                    initialdir='/Users/averygreen/Documents/Viaex/SEM',
    #                                    parent=root)
    new_image = plt.imread(img_path + '/' + pic_name + '.tiff')


    # Phenom and Zeiss have different scale locations.
    phenom_mag_bbox = np.array([378, 1029, 478, 1054]) * new_image.shape[1] / 1024
    # zeiss_mag_bbox = np.array([1420, 1400, 1630, 1460]) * new_image.shape[0] / 1536
    mag_bbox = phenom_mag_bbox.astype(int)
    mag_image = new_image[mag_bbox[1]:mag_bbox[3], mag_bbox[0]:mag_bbox[2]]
    mag_fname = img_path + '/' + 'mag_inter.tif'
    plt.imsave(arr=mag_image, fname=mag_fname, dpi=72)
    mag_image = Image.open(mag_fname)

    mag_text = pytesseract.image_to_string(mag_image)
    mag_text = re.sub(' ', '', mag_text)
    mag_text = re.sub('S', '5', mag_text)
    mag_text = re.sub('O', '0', mag_text)
    mag_text = re.sub('D', '0', mag_text)
    mag_text_split = re.search('[a-zA-Z]+', mag_text).start()
    mag_text = [mag_text[:mag_text_split], mag_text[mag_text_split:]]


    # Use mag scaler to calibrate image scales
    # Comes from M = 5400x image that has 10 um / 205 pix
    # Divide mag_scaler by M_new to get new pixel scaling.
    mag_scaler = (10/205)*5400
    pix_to_um = mag_scaler/float(mag_text[0])

    ## THIS PART IS NOT NECESSARY FOR PHENOM. MAG ONLY EXPRESSED IN X
    # if 'K' in mag_text[1]:
    #     pix_to_um *= pow(10, -3)
    # elif 'M' in mag_text[1]:
    #     pix_to_um *= pow(10, -6)

    diameters = np.array(csv_data[1:, 0], dtype=float)
    freqs = np.array(csv_data[1:, 1], dtype=float)
    freqs = freqs/sum(freqs)

    last_datapt_index = max(np.nonzero(freqs)[0])
    diameters = diameters[:last_datapt_index]
    freqs = freqs[:last_datapt_index]

    diameters = diameters * pix_to_um

    csv_file = open(NewPath + '/' + pic_name + '.csv', 'w+')
    csv_writer = csv.writer(csv_file)
    csv_output = np.array([freqs, diameters])
    csv_output = np.transpose(csv_output)
    csv_output = np.around(csv_output, decimals=3)
    csv_writer.writerow(['Frequency', 'Diameter'])
    csv_writer.writerow(['norm', 'um'])
    csv_writer.writerows(csv_output)

    AllData.append([diameters, freqs, label])

    test = 1

    # max_diameter_index = np.argmax(diameters)
    # diameters = diameters[:max_diameter_index]
    # freqs = freqs[:max_diameter_index]

    axes = plt.gca()
    axes.fill_between(diameters, 0, freqs)
    axes.set_xlabel('Fiber Diameter (um)')
    axes.set_ylabel('Frequency (norm)')
    # plt.hist(freqs, diameters)

    test = 1

    plt.savefig(NewPath + '/' + pic_name + '.png', dpi=144)

    plt.cla()

    print('Finished ' + pic_name)

for histdata in AllData:

    axes = plt.gca()
    axes.plot(histdata[0], histdata[1], label=histdata[2])
    axes.set_xlabel('Fiber Diameter (um)')
    axes.set_ylabel('Frequency (norm)')
    axes.legend()

plt.savefig(NewPath + '/All_Data.png', dpi=144)

plt.cla()

plt.close(plt.gcf())

test = 1

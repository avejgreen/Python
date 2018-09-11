import numpy as np
import glob, csv, re
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

np.set_printoptions(precision=4)

input_hist_files = filedialog.askopenfiles(title='Choose histograms to combine',
                                           parent=root)

input_data = []
input_headers = []
for input_file in input_hist_files:
    reader = csv.reader(open(input_file.name))
    csv_data = list(reader)
    input_headers.append(csv_data[0:2])
    array_data = np.array([list(map(float, y)) for y in csv_data[2:]])
    input_data.append(array_data.transpose())

input_sets_max_x = [np.max(input_data[x][0]) for x in range(len(input_data))]

meanset_Dx = np.mean([x[0][1] for x in input_data])
meanset_max_x = meanset_Dx * np.ceil(np.max(input_sets_max_x) / meanset_Dx)
meanset_nbins = int(np.round(meanset_max_x / meanset_Dx))
meanset_xvals = np.linspace(0, meanset_max_x, meanset_nbins+1)
meanset_yvals = np.zeros(len(meanset_xvals))

# Go along meanset bins
for meanset_bin in range(1, meanset_nbins):
    meanset_bin_x0 = meanset_xvals[meanset_bin-1]
    meanset_bin_x1 = meanset_xvals[meanset_bin]

    # Go along input sets, find values in the meanset bin
    for input_set in input_data:
        input_set_Dx = input_set[0][1] - input_set[0][0]
        input_set_inner_nodes = np.where([meanset_bin_x0 < x < meanset_bin_x1 for x in input_set[0]])[0]
        input_set_lesser_nodes = np.where(input_set[0] <= meanset_bin_x0)[0]
        input_set_greater_nodes = np.where(input_set[0] >= meanset_bin_x1)[0]

        # Infimum node guaranteed by definition of inner nodes
        # Possibilities for bin contribution:
        # 0. Infimum, 0 inner, no supremum
        #   End reached. No contribution. Break.
        # 1. Infimum, 0 inner, supremum
        #   Contribution is mean bin width multiplied by supremum y value
        # 2. Infimum, n inner, no supremum
        #   Contribution is mean bin x0 to inner x0 times input_set y(x) plus
        #   input_set_delta_x times (y(x1) + y(x2) + ... y(xn))
        # 3. Infimum, n inner, supremum
        #   Contribution is mean bin x0 to inner x0 times input_set y(x) plus
        #   input_set_delta_x times (y(x1) + y(x2) + ... y(xn)) plus
        #   inner xn to mean bin x1 times y(supremum)

        if len(input_set_inner_nodes) == 0 and len(input_set_greater_nodes) == 0:
            break

        elif len(input_set_inner_nodes) == 0:
            meanset_yvals[meanset_bin] += (meanset_Dx / input_set_Dx) * input_set[1][input_set_greater_nodes][0]

        else:
            meanset_yvals[meanset_bin] += ((input_set[0][input_set_inner_nodes[0]] - meanset_bin_x0) / input_set_Dx) * \
                                          input_set[1][input_set_inner_nodes[0]]

            for inner_node in range(1, len(input_set_inner_nodes)):
                meanset_yvals[meanset_bin] += input_set[1][input_set_inner_nodes[inner_node]]

            if len(input_set_greater_nodes) == 0:
                break

            else:
                meanset_yvals[meanset_bin] += ((meanset_bin_x1 - input_set[0][input_set_inner_nodes[-1]]) /
                                               input_set_Dx) * input_set[1][input_set_greater_nodes[0]]

        test = 1

meanset_yvals = meanset_yvals / len(input_data)

axes = plt.gca()
axes.fill_between(meanset_xvals, 0, meanset_yvals)
axes.set_xlabel('Fiber Diameter (um)')
axes.set_ylabel('Frequency (norm)')

output_fullname = '_'.join(input_hist_files[0].name.split('_')[:-1])
plt.savefig(output_fullname + '.png', dpi=144)
plt.close(plt.gcf())

csv_file = open(output_fullname + '.csv', 'w+')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Diameter', 'Frequency'])
csv_writer.writerow(['um', 'norm'])
csv_output = np.array([meanset_xvals, meanset_yvals])
csv_output = np.transpose(csv_output)
csv_output = np.around(csv_output, decimals=4)
csv_writer.writerows(csv_output)
csv_file.close()


test = 1
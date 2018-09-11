import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
# from matplotlib.animation import FuncAnimation
# import sys, time

def main():

    ind_fig = plt.figure(figsize=(3, 8))
    ind_values = [90,35,45,10]

    # Want bars to take up 45%, radials 45%, labels 10% of height
    rect_button_down = [.05,0,.425,.05]
    rect_button_up = [.525,0,.425,.05]
    rect_radial = [0,0.1,1,.3]
    rect_bar = [.15,.5,.8,.45]

    axes_button_down = plt.axes(rect_button_down)
    axes_button_up = plt.axes(rect_button_up)
    axes_bar = plt.axes(rect_bar)
    axes_radial = plt.axes(rect_radial, polar=True)
    axes_radial.set_thetamin(-90)
    axes_radial.set_thetamax(90)
    axes_radial.set_rticks([])
    axes_radial.set_xticks(np.arange(-90,91,36)*np.pi/180)
    axes_radial.set_xticklabels(['0','20','40','60','80','100'])

    def make_plot():
        x = np.arange(0, 5, 0.1)
        y = np.sin(x)
        plt.plot(x, y)

    def make_bar(values=ind_values):
        plt.sca(axes_bar)
        positions = [0, 1, 2, 3]
        colors = ['r', 'b', 'y', 'g']
        plt.bar(positions, values, color=colors)
        axes_bar.set_title('Bar Chart')
        axes_bar.set_ylim([0,120])
        axes_bar.set_yticks([0,20,40,60,80,100])
        # axes_bar.set_ylabel('Percent usage')
        axes_bar.set_xticklabels(['Cat1','Cat2','Cat3','Cat4','Cat5'])
        for cat in range(4):
            plt.text(cat,110,str(values[cat]),horizontalalignment='center')

    def make_radial(values=ind_values):
        plt.sca(axes_radial)
        colors = ['r', 'b', 'y', 'g']
        thetas = np.pi * (np.array(values) / 100 - 0.5)
        plt.plot([0, thetas[0]], [0, 1], colors[0],
                 [0, thetas[1]], [0, 1], colors[1],
                 [0, thetas[2]], [0, 1], colors[2],
                 [0, thetas[3]], [0, 1], colors[3])

    def update_plots(new_value):

        axes_bar.texts[0].set_text("%.1f" % new_value)
        axes_bar.containers[0][0].set_height(new_value)
        axes_radial.lines[0].set_xdata([0, np.pi * (new_value / 100 - 0.5)])
        plt.draw()

    def button_up_fcn(event):
        old_value = ind_values[0]
        new_value = old_value + 20
        if new_value > 100:
            new_value = 100
        ind_values[0] = new_value

        update_plots(new_value)

    def button_down_fcn(event):
        old_value = ind_values[0]
        new_value = old_value - 20
        if new_value < 0:
            new_value = 0
        ind_values[0] = new_value

        update_plots(new_value)

    make_bar(ind_values)
    make_radial(ind_values)

    button_down = Button(axes_button_down, 'Down')
    button_up = Button(axes_button_up, 'Up')

    button_down.on_clicked(button_down_fcn)
    button_up.on_clicked(button_up_fcn)

    plt.show()

main()

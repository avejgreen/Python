import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import sys, time

class Ind(object):

    def __init__(self, **kwargs):

        def set_traits():

            self.ind_traits = {'labels': ['Ind1', 'Ind2', 'Ind3', 'Ind4'],
                               'values': [50, 80, 30, 40]}

            for kwarg in self.ind_traits:
                if kwarg in kwargs:
                    self.ind_traits[kwarg] = kwargs.pop(kwarg)

            # If len(labels) != len(values), change values
            num_labels = len(self.ind_traits['labels'])
            num_values = len(self.ind_traits['values'])
            if num_labels > num_values:
                # Increase values
                for i in range(0, num_labels - num_values):
                    self.ind_traits['values'].append(0)
            elif num_labels < num_values:
                # Truncate values
                self.ind_traits['values'] = self.ind_traits['values'][:num_labels]

        def make_plot():
            x = np.arange(0, 5, 0.1)
            y = np.sin(x)
            plt.plot(x, y)

        def make_bar():

            rect_bar = [.15, .5, .8, .45]
            axes_bar = plt.axes(rect_bar)

            # plt.sca(axes_bar)

            positions = [0, 1, 2, 3]
            values = self.ind_traits['values']
            colors = ['r', 'b', 'y', 'g']
            plt.bar(positions, values, color=colors)

            axes_bar.set_title('Bar Chart')
            axes_bar.set_ylim([0,120])
            axes_bar.set_yticks([0,20,40,60,80,100])
            # axes_bar.set_ylabel('Percent usage')
            axes_bar.set_xticklabels(['Cat1','Cat2','Cat3','Cat4','Cat5'])

            for cat in range(4):
                plt.text(cat, 110, str(values[cat]), horizontalalignment='center')

            return axes_bar

        def make_radial():

            rect_radial = [0, 0.1, 1, .3]
            axes_radial = plt.axes(rect_radial, polar=True)
            axes_radial.set_thetamin(-90)
            axes_radial.set_thetamax(90)
            axes_radial.set_rticks([])
            axes_radial.set_xticks(np.arange(-90, 91, 36) * np.pi / 180)
            axes_radial.set_xticklabels(['0', '20', '40', '60', '80', '100'])

            values = self.ind_traits['values']
            colors = ['r', 'b', 'y', 'g']

            thetas = np.pi * (np.array(values) / 100 - 0.5)
            plt.plot([0, thetas[0]], [0, 1], colors[0],
                     [0, thetas[1]], [0, 1], colors[1],
                     [0, thetas[2]], [0, 1], colors[2],
                     [0, thetas[3]], [0, 1], colors[3])

            return axes_radial

        def make_buttons():

            # Want bars to take up 45%, radials 45%, labels 10% of height
            rect_button_down = [.05, 0, .425, .05]
            rect_button_up = [.525, 0, .425, .05]

            axes_button_down = plt.axes(rect_button_down)
            axes_button_up = plt.axes(rect_button_up)

            button_down = Button(axes_button_down, 'Down')
            button_up = Button(axes_button_up, 'Up')

            button_down.on_clicked(self.button_down_fcn)
            button_up.on_clicked(self.button_up_fcn)

            return [button_down, button_up]

        set_traits()

        self.figure = plt.figure(**kwargs)
        self.axes_bar = make_bar()
        self.axes_radial = make_radial()
        buttons = make_buttons()
        self.button_down = buttons[0]
        self.button_up = buttons[1]

        plt.show()

    def button_up_fcn(self, event):
        old_value = self.ind_traits['values'][0]
        # old_height = axes_bar.containers[0][0].get_height()
        new_value = old_value + 20
        if new_value > 100:
            new_value = 100
        self.ind_traits['values'][0] = new_value

        self.update_plots(old_value, new_value)
        # update_plots(old_value, new_value)

    def button_down_fcn(self, event):
        old_value = self.ind_traits['values'][0]
        # old_height = axes_bar.containers[0][0].get_height()
        new_value = old_value - 20
        if new_value < 0:
            new_value = 0
        self.ind_traits['values'][0] = new_value

        self.update_plots(old_value, new_value)
        # update_plots(old_value, new_value)

    def update_plots(self, old_value, new_value):

        inter_range = np.arange(old_value, new_value, (new_value-old_value)/100)
        inter_range = np.append(inter_range, new_value)

        for inter_value in inter_range:
            self.axes_bar.texts[0].set_text("%.1f" % inter_value)
            self.axes_bar.containers[0][0].set_height(inter_value)
            self.axes_radial.lines[0].set_xdata([0, np.pi * (inter_value / 100 - 0.5)])
            plt.draw()
            plt.pause(.01)

        test = 1

        # def do_animation(value):
        #     axes_bar.texts[0].set_text("%.1f" % value)
        #     axes_bar.containers[0][0].set_height(value)
        #     axes_radial.lines[0].set_xdata([0, np.pi * (value / 100 - 0.5)])
        #     plt.draw()
        #     plt.pause(0.1)
        #
        # def gen_values():
        #     values = np.append(np.round(
        #         np.arange(old_value, new_value, (new_value - old_value) / 100)), new_value)
        #     for i in values:
        #         yield i
        #
        # ani = FuncAnimation(ind_fig, do_animation, gen_values, interval=10, repeat=False)



new_ind = Ind(labels=['Ind1', 'Ind2', 'Ind3', 'Ind4'], figsize=(3, 8))

# plt.axis([0, 10, 0, 1])
#
# for i in range(10):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.05)
#
# # plt.show()




# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
# fig, ax = plt.subplots()
# line, = ax.plot(np.random.rand(10))
# ax.set_ylim(0, 1)
#
#
# def update(data):
#     line.set_ydata(data)
#     return line,
#
#
# def data_gen():
#     while True:
#         yield np.random.rand(10)
#
# ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
# plt.show()
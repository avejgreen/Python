import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import sys, time

"""
Ind_Figure requires a LIST of ind_indicators
Indicator names must be unique
kwargs must be kwargs for pyplot figure
"""

class Ind_Figure(object):

    def __init__(self, indicators=None, figure_kwargs=None,
                 axes_bar_kwargs=None, bar_kwargs=None,
                 axes_radial_kwargs=None, radial_kwargs=None,
                 button_group_kwargs=None):

        self.cmap = plt.get_cmap('Set1')
        self.set_indicators(indicators)
        self.make_figure(figure_kwargs)
        self.make_axes_bar(axes_bar_kwargs)
        self.make_bar(bar_kwargs)
        self.make_axes_radial(axes_radial_kwargs)
        self.make_radial(radial_kwargs)
        self.make_buttons(button_group_kwargs)

        self.ani = None

        plt.show()

    def set_indicators(self, inds):
        if inds is None:
            self.indicators = [Ind_Indicator()]
        elif all(isinstance(i, Ind_Indicator) for i in inds):
            self.indicators = inds
        else:
            self.indicators = [Ind_Indicator()]

    def make_figure(self, kwargs):
        if kwargs is None or 'figsize' not in kwargs:
            self.figure = plt.figure(figsize=(3, 8))
        else:
            self.figure = plt.figure(**kwargs)

    def make_axes_bar(self, kwargs):
        rect_bar = [.15, .55, .8, .4]
        axes_bar = plt.axes(rect_bar)
        axes_bar.set_title('Bar Chart')
        axes_bar.set_ylim([0, 120])
        axes_bar.set_yticks([0, 20, 40, 60, 80, 100])
        self.axes_bar = axes_bar

    def make_bar(self, kwargs):

        positions = list(range(len(self.indicators)))
        values = [i.value for i in self.indicators]
        tick_label = [i.name for i in self.indicators]
        colors = self.cmap.colors[:len(self.indicators)]

        bar = plt.bar(positions, values, color=colors, tick_label=tick_label)

        max_max = max([i.max for i in self.indicators])
        for pos, val in zip(positions, values):
            plt.text(pos, max_max + 10, val, horizontalalignment='center')

        self.bar = bar

    def make_axes_radial(self, kwargs):
        rect_radial = [0, 0.15, 1, .3]
        axes_radial = plt.axes(rect_radial, polar=True)
        axes_radial.set_thetamin(-90)
        axes_radial.set_thetamax(90)
        axes_radial.set_rticks([])
        axes_radial.set_xticks(np.arange(-90, 91, 36) * np.pi / 180)
        axes_radial.set_xticklabels(['0', '20', '40', '60', '80', '100'])
        self.axes_radial = axes_radial

    def make_radial(self, kwargs):

        values = [i.value for i in self.indicators]
        thetas = np.pi * (np.array(values) / 100 - 0.5)
        colors = self.cmap.colors[:len(self.indicators)]
        radial = []


        for theta, color in zip(thetas, colors):
            radial += plt.plot([0, theta], [0, 1], color=color)

        self.radial = radial

    def make_buttons(self, kwargs):

        gap = 0.05
        num_inds = len(self.indicators)
        names = [i.name for i in self.indicators]
        colors = self.cmap.colors[:len(self.indicators)]

        width = (1 - ((num_inds + 1) * gap)) / num_inds
        height = 0.03

        x_pos = []
        for i in range(num_inds):
            x_pos.append(gap + (width + gap) * i)

        axes_buttons = []
        buttons = []
        for x, name, color in zip(x_pos, names, colors):

            axes_buttons.append(plt.axes([x, 0.04, width, height], label=name + '_Up'))
            buttons.append(Button(axes_buttons[-1], 'Up', color=color))
            buttons[-1].on_clicked(self.button_up_fcn)

            axes_buttons.append(plt.axes([x, 0, width, height], label=name+'_Down'))
            buttons.append(Button(axes_buttons[-1], 'Down', color=color))
            buttons[-1].on_clicked(self.button_down_fcn)

        self.axes_buttons = axes_buttons
        self.buttons = buttons

    def button_up_fcn(self, event):

        ind_str = event.inaxes._label[:-3]

        ind_booleans = list(map(lambda x: x.name == ind_str, self.indicators))
        ind_index = ind_booleans.index(True)
        ind = self.indicators[ind_index]

        old_value = ind.value
        if old_value == ind.max:
            pass
        new_value = old_value + ind.range * ind.delta
        if new_value > ind.max:
            new_value = ind.max
        ind.value = new_value
        self.indicators[ind_index] = ind

        self.update_plots(ind_index, old_value, new_value)
        # update_plots(old_value, new_value)

    def button_down_fcn(self, event):
        ind_str = event.inaxes._label[:-5]

        ind_booleans = list(map(lambda x: x.name == ind_str, self.indicators))
        ind_index = ind_booleans.index(True)
        ind = self.indicators[ind_index]

        old_value = ind.value
        if old_value == ind.min:
            pass
        new_value = old_value - ind.delta * ind.range
        if new_value < ind.min:
            new_value = ind.min
        ind.value = new_value
        self.indicators[ind_index] = ind

        self.update_plots(ind_index, old_value, new_value)
        # update_plots(old_value, new_value)

    def update_plots(self, ind_index, old_value, new_value):

        inter_range = np.arange(old_value, new_value,
                                (new_value-old_value)/self.indicators[ind_index].delta_steps)
        inter_range = np.append(inter_range, new_value)

        for inter_value in inter_range:
            self.axes_bar.texts[ind_index].set_text("%.1f" % inter_value)
            self.axes_bar.containers[0][ind_index].set_height(inter_value)
            self.axes_radial.lines[ind_index].set_xdata([0, np.pi * (inter_value / 100 - 0.5)])
            plt.draw()
            plt.pause(.1)

class Ind_Indicator(object):

    def __init__(self, name='Test Indicator', value=50, **kwargs):

        """
        Attributes:
            value       - curent value
            min_value   - minimum value
            max_value   - maximum value
            delta       - change of value when button is pressed
            delta_steps - steps shown in animation of value change
        """

        attributes = {'name': name,
                      'value': value}

        kw_attributes = {'min': 0,
                         'max': 100,
                         'delta': 0.2,
                         'delta_steps': 10}

        for key in kw_attributes:
            if key in kwargs:
                kw_attributes[key] = kwargs[key]

        attributes.update(kw_attributes)

        self.__dict__ = attributes

        if self.min > self.max:
            self.max = self.min + 10
        self.range = self.max - self.min
        if self.value < self.min or self.value > self.max:
            self.value = self.min + self.range/2
        if self.delta >= 1 or self.delta <= 0:
            self.delta = 0.2
        if type(self.delta_steps) is not int:
            self.delta_steps = 1

        test = 1

Ind1 = Ind_Indicator('Ind1')
Ind2 = Ind_Indicator('Ind2', 20, delta_steps=20)
Ind3 = Ind_Indicator('Ind3', 60)
Ind4 = Ind_Indicator('Hi')
Ind5 = Ind_Indicator('Butts', 100)

new_ind = Ind_Figure([Ind1, Ind2, Ind3, Ind4, Ind5])
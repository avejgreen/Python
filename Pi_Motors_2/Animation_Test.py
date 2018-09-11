import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# def update_line(num, data, line):
#     line.set_data(data[..., :num])
#     return line,
#
# fig1 = plt.figure()
#
# data = np.random.rand(2, 25)
# l, = plt.plot([], [], 'r-')
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('test')
# line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
#                                    interval=50, blit=True)


#
# def func(frame):
#     x = np.linspace(1,10,10)
#     y = np.linspace(1,frame,10)
#     line_plot.set_data(x,y)
#
#     return line_plot,
#
# def init_func():
#     x_bar = [0, 1, 2, 3]
#     height = [20, 30, 60, 90]
#     bar_plot = plt.bar(x_bar, height, align='center')
#
#     x = np.arange(1,10)
#     y = np.arange(1,10)
#     line_plot = plt.plot(x,y)
#
#     return bar_plot, line_plot
#
# fig = plt.figure()
# bar_plot, line_plot = init_func()
# frames = np.arange(1,10)
#
# fargs = ()
#
# save_count = 0
# interval = 1000
# repeat_delay = 1000
# repeat = True
# blit = True
# kwargs = {'save_count': save_count,
#           'interval': interval,
#           'repeat_delay': repeat_delay,
#           'repeat': repeat,
#           'blit': blit}
#
# ani = animation.FuncAnimation(fig, func, frames, *fargs, **kwargs)



plt.show()
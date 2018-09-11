import numpy as np
import tkinter as tk

# Ray Tracing: Generate canvas class object for line vector input.
# class RayCanvas(tk.Canvas):
#
#     def __init__(self, master):
#         tk.Canvas.__init__(master)
#         self.setvar(self, 'width', 100)
#         self.setvar(self, 'height', 100)

class ray(object):

    def __init__(self):
        self.p0 = None
        self.p1 = None
        self.t0 = 0
        self.t1 = None
        self.v = None
        pass

    def set_p0(self, p0_input):
        self.p0 = p0_input

    def set_p1(self, p1_input):
        self.p1 = p1_input

    def set_t0(self, t0_input):
        self.t0 = t0_input

    def set_t1(self, t1_input):
        self.t1 = t1_input

    def set_v(self, v_input):
        self.v = v_input

    def set_name(self, name_input):
        self.name = name_input

    def get_p0(self):
        return self.p0

    def get_p1(self):
        return self.p1

    def get_t0(self):
        return self.t0

    def get_t1(self):
        return self.t1

    def get_v(self):
        return self.v

    def get_name(self):
        return self.name


def motion_handle(event):
    started_flag = event.widget.ray_started_flag
    real_x = event.x
    real_y = canvas_height + 1 - event.y
    canvas.itemconfigure(position_text, text=str(real_x) + ',' + str(real_y))

    # If the ray is being drawn, redraw its line
    if started_flag:
        line_tag = all_rays[-1].get_name()
        p0 = all_rays[-1].get_p0()
        canvas.coords(line_tag, p0[0], canvas_height - p0[1] + 1, event.x, event.y)

def mouse_button_handle(event):
    # Get the new point.
    started_flag = event.widget.ray_started_flag
    real_x = event.x
    real_y = canvas_height + 1 - event.y
    new_point = np.array([real_x, real_y])

    if not started_flag:
        # Ray is new. Draw trivial line. Add it to the ray list.
        started_flag = True
        new_ray = ray()
        new_ray.set_p0(new_point)
        new_ray.set_name('ray' + str(len(all_rays)))
        all_rays.append(new_ray)
        canvas.create_line(event.x, event.y, event.x, event.y,
                           fill='black', width=2, tags=new_ray.get_name())

    elif started_flag:
        # Ray is ending. Add the last point, compute v and t1
        started_flag = False
        all_rays[-1].set_p1(new_point)
        v_new = all_rays[-1].get_p1() - all_rays[-1].get_p0()
        t1_new = np.linalg.norm(v_new)
        all_rays[-1].set_t1(t1_new)
        all_rays[-1].set_v(v_new/t1_new)

    event.widget.ray_started_flag = started_flag

if __name__ == '__main__':

    root = tk.Tk()

    all_rays = []

    canvas_width = 500
    canvas_height = 500
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.ray_started_flag = False
    canvas.bind('<Motion>', motion_handle)
    canvas.bind('<Button-1>', mouse_button_handle)

    position_text = canvas.create_text(2, canvas_height, anchor=tk.SW, text='Hello')

    canvas.grid()



    tk.mainloop()
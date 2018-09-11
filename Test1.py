import numpy as np
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox


class Rectangle(object):

    def __init__(self, **kwargs):
        self.tag = kwargs['tag']
        self.anchor = kwargs['anchor']
        self.coordinates = kwargs['coordinates']
        self.voltage = None
        self.x_length = None
        self.y_length = None
        self.area = None
        self.perimeter = None
        self.charge_density = None

    def set_size(self):

        self.x_length = self.coordinates[2] - self.coordinates[0]
        self.y_length = self.coordinates[3] - self.coordinates[1]
        self.area = self.x_length * self.y_length

        perimeter = np.array([np.arange(self.coordinates[0], self.coordinates[2]),
                             np.ones(self.x_length, dtype=int) * self.coordinates[1]])
        perimeter = np.append(perimeter,
                              np.array([np.ones(self.y_length, dtype=int) * self.coordinates[2],
                                        np.arange(self.coordinates[1], self.coordinates[3])]),
                              axis=1)
        perimeter = np.append(perimeter,
                              np.array([np.arange(self.coordinates[2], self.coordinates[0], -1),
                                        np.ones(self.x_length, dtype=int) * self.coordinates[3]]),
                              axis=1)
        perimeter = np.append(perimeter,
                              np.array([np.ones(self.y_length, dtype=int) * self.coordinates[0],
                                        np.arange(self.coordinates[3], self.coordinates[1], -1)]),
                              axis=1)
        self.perimeter = perimeter


    def set_charge_density(self):

        matrix_1 = np.kron(np.ones([np.shape(self.perimeter)[1], 1, 1]),
                           np.reshape(self.perimeter, [1, np.shape(self.perimeter)[1], 2]))
        matrix_2 = np.kron(np.ones([1, np.shape(self.perimeter)[1], 1]),
                           np.reshape(self.perimeter, [np.shape(self.perimeter)[1], 1, 2]))
        matrix_3 = np.linalg.norm(matrix_2 - matrix_1, axis=2)
        matrix_4 = np.divide(1, matrix_3)
        matrix_5 = np.linalg.inv(matrix_4)

        progress_message = messagebox.showinfo("Information", "Informative message", parent=root)
        for i in range(np.shape(inner_points)[1]):
            if i == np.round(np.shape(inner_points)[1] / 10):
                test = 1
            for j in range(np.shape(self.perimeter)[1]):
                M[i, j] = 1/np.linalg.norm(inner_points[:, i] - self.perimeter[:, j])
                test = 1

        Minv = np.linalg.inv(M)

        charge_density = np.matmul(Minv, np.ones(1))

        test = 1

def pause_fcn():
    test = 1
    pass


def enter_fcn(event):
    test = 1
    pass


def click_fcn(event):
    x = event.x
    y = event.y

    pause_bbox = canvas.coords('button_pause')
    potential_bbox = canvas.coords('button_potential')
    field_bbox = canvas.coords('button_field')
    if pause_bbox[0] <= x < pause_bbox[2] and pause_bbox[1] <= y < pause_bbox[3]:
        test = 1
    elif potential_bbox[0] <= x < potential_bbox[2] and potential_bbox[1] <= y < potential_bbox[3]:
        test = 1
    elif field_bbox[0] <= x < field_bbox[2] and field_bbox[1] <= y < field_bbox[3]:
        test = 1

    else:
        # Creating a rectangle
        if not canvas.drawing_rect:
            # Create rectangle with tag 'rect_[number of canvas items + 1]'
            # such that the new rectangle is tagged as such, and shows what item number
            # it was created as.
            rect_tag = 'rect_' + str(canvas.find_all()[-1] + 1)
            new_rect = Rectangle(tag=rect_tag, anchor=[x, y], coordinates=[x, y, x, y])
            rect_dict[rect_tag] = new_rect

            canvas.create_rectangle(x, y, x, y, tag=rect_tag)
            canvas.drawing_rect = True

        elif canvas.drawing_rect:
            rect_tag = list(rect_dict.keys())[-1]
            current_rect = rect_dict[rect_tag]
            new_coords = mod_rectangle(current_rect.coordinates, current_rect.anchor, x, y)

            canvas.coords(rect_tag, new_coords)

            # Only finish the rectangle if its minimum edge size is >= 3
            # Otherwise, there's no body for voltage
            if np.abs(new_coords[2] - new_coords[0]) < 3 or np.abs(new_coords[3] - new_coords[1]) < 3:
                pass
            else:
                canvas.drawing_rect = False
                voltage = simpledialog.askstring("Input", "Enter voltage of rectangle", parent=root)
                current_rect.voltage = float(voltage)
                current_rect.set_size()
                current_rect.set_charge_density()

                rect_dict[rect_tag] = current_rect

        test = 1
    pass


def mod_rectangle(old_coords, rect_anchor, x, y):

    new_coords = old_coords[:]

    if x < rect_anchor[0]:
        # New point is to the left of the anchor
        new_coords[0] = x
        new_coords[2] = rect_anchor[0]
    else:
        new_coords[2] = x
        new_coords[0] = rect_anchor[0]

    if y < rect_anchor[1]:
        # New point is above the anchor
        new_coords[1] = y
        new_coords[3] = rect_anchor[1]
    else:
        new_coords[3] = y
        new_coords[1] = rect_anchor[1]

    return new_coords


def motion_fcn(event):
    x = event.x
    y = event.y
    canvas.itemconfigure('position', text='(' + str(x) + ', ' + str(y) + ')')

    if canvas.drawing_rect:
        rect_tag = list(rect_dict.keys())[-1]
        current_rect = rect_dict[rect_tag]
        current_rect.coordinates = mod_rectangle(current_rect.coordinates, current_rect.anchor, x, y)
        rect_dict[rect_tag] = current_rect

        canvas.coords(rect_tag, current_rect.coordinates)
    pass


def create_button(x0, y0, x1, y1, button_text):
    canvas.create_rectangle(x0, y0, x1, y1, tag='button_' + button_text)
    canvas.create_text(np.floor((x0+x1)/2), np.floor((y0+y1)/2), text=button_text)


def create_canvas_items():

    canvas.drawing_rect = False
    canvas.rect_anchor = (0, 0)

    canvas.create_text(2, 598, anchor=tk.SW, text='(0, 0)', tag='position')
    create_button(725, 550, 798, 598, 'pause')
    create_button(300, 550, 375, 598, 'potential')
    create_button(425, 550, 500, 598, 'field')

    canvas.bind('<Enter>', enter_fcn)
    canvas.bind('<Motion>', motion_fcn)
    canvas.bind('<1>', click_fcn)

    canvas.grid()

    pass

root = tk.Tk()
root.configure(bd=0)
root.focus()
root.attributes("-topmost", True)
root.after(1000, lambda: root.attributes("-topmost", False))

canvas = tk.Canvas(root, width=800, height=600)
canvas.configure(bd=0)

rect_dict = {}
display_mode = 'potential'
canvas.drawing_rect = False
create_canvas_items()

# root.attributes('-topmost', True)

root.mainloop()
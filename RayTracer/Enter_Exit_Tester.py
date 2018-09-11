import tkinter as tk

def motion_cmd(event):

    canvas.itemconfigure(position_text, text=str(event.x)+', '+str(canvas_height + 1 - event.y))

root = tk.Tk()

canvas_width = 200
canvas_height = 200
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bd=0)

position_text = canvas.create_text(2, canvas_height, anchor=tk.SW, text='Hello')

canvas.bind('<Motion>', motion_cmd)
# canvas.scale()
canvas.grid()

root.mainloop()

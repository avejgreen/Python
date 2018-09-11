from tkinter import *
from PIL import Image, ImageTk

class App:

    def __init__(self, master):

        self.frame = Frame(master)
        self.frame.grid()

        self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.grid(row=0, column=0)

        self.hi_there = Button(self.frame, text="Hello", command=self.say_hi)
        self.hi_there.grid(row=1, column=1)

        self.label1 = Label(self.frame, text='Bobo')
        self.label1.grid(row=0, column=1)

        icon_path = '/Users/averygreen/PycharmProjects/MazeGame/Features/'
        # grass_icon = ImageTk.PhotoImage(Image.open(icon_path + 'grass.gif'))
        grass_icon = PhotoImage(file=icon_path + 'grass.gif')
        self.label2 = Label(self.frame, image=grass_icon)
        self.label2.image = grass_icon
        self.label2.grid(row=1, column=0)

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below



# frame = tk.Frame()
# frame.grid()
#
# grass_name = '/Users/averygreen/PycharmProjects/MazeGame/Features/grass.gif'
# grass_image = tk.PhotoImage(name=grass_name)
#
# w1 = tk.Label(frame, image=grass_image)
# w2 = tk.Label(frame, image=grass_image)
#
# w1.grid(row=0, column=0)
# w2.grid(row=1, column=1)
#
# # frame.grid_propagate(0)
#
# frame.mainloop()
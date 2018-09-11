import tkinter, re, warnings

root = tkinter.Tk()

class Indicators(tkinter.Canvas):

    def __init__(self, master=None, **keyword_parameters):

        #####
        # Initiate. Write down names and values, assign unique number identifiers
        # Use the canvas constructor with remaining keyword_parameters
        # Define the geometry, create bars and radials
        #####

        # Write names and values of categories, assign ID ints
        if 'ind_names' in keyword_parameters:
            self.ind_names = keyword_parameters.pop('ind_names')
        else:
            self.ind_names = ['Test_Indicator']
        if 'ind_values' in keyword_parameters:
            self.ind_values = keyword_parameters.pop('ind_values')
        else:
            self.ind_values = [0]

        self.ind_numbers = []
        for i in range(len(self.ind_names)):
            self.ind_numbers.append(i)

        # Trim or expand values to match names
        if len(self.ind_values) > len(self.ind_names):
            self.ind_values = self.ind_values[:len(self.ind_names)]
            warnings.warn('More values than categories entered. Removed latter values.')
        elif len(self.ind_values) < len(self.ind_names):
            for i in range(len(self.ind_names)-len(self.ind_values)):
                self.ind_values.append(0)

        # Generate canvas
        tkinter.Canvas.__init__(self, master, keyword_parameters)

        # Default geometry:
        #   bar section:
        #       300 in height (50 for axis, 200 for bar, 50 for label)
        #       100 per bar plus 50 in width
        #   radial section:
        #       100 in height
        #       100 in width
        #   totals:
        #       400 in height, 100*bars + 50 in width

        self.create_line(50, 250, 50, 50)
        self.create_line(50, 250, 150, 250)

        self.create_text(50, 300, text='Test1')
        self.create_text(50, 50, text='Test2')
        self.create_arc(50, 400, 150, 300)

        test = 1

def callback(event):

    geo_string = root.nametowidget('frame').nametowidget('ind_canvas').winfo_geometry()
    geo_list = re.findall('\d+', geo_string)
    print(geo_list)

def setup_widgets():

    root.grid_propagate(False)

    frame = tkinter.Frame(root, height=200, width=200, bg="gray80", name='frame')

    frame.grid()
    frame.bind("<Button-1>", callback)

    hello_label = tkinter.Label(frame, text="Hello, World", bg="gray80", fg="white", bd=1, name='hello_label')
    hello_label.grid(row=0, column=0)

    button = tkinter.Button(frame, text="Exit", bg="gray80", fg="white", bd=1, command=root.destroy, name='button')
    button.grid(row=1, column=0)

    bar_indicator = tkinter.Label(frame, text="0 %", name='bar_indicator')
    bar_indicator.grid(row=0, column=1)

    # ind_canvas = Indicators()
    ind_canvas = Indicators(frame, name='ind_canvas', ind_names=['Motor1', 'Motor2', 'Motor3'], ind_values=[100, 50])
    ind_canvas.grid(row=1, column=1)

    root.update()

setup_widgets()

root.mainloop()

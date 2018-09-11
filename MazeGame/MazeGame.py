from tkinter import *

class board:

    def __init__(self, master, cells=11, features=[[], []]):

        # Generate the frame with key bindings
        self.frame = Frame(master, name='frame')
        self.frame.grid()
        # self.frame.bind('<1>', self.keypress)
        # self.frame.bind('<Key>', self.keypress)
        self.frame.focus_set()

        # Include dictionary icons as an attribute
        icon_path = '/Users/averygreen/PycharmProjects/MazeGame/Features/'
        self.icons = {}
        self.icons['grass'] = PhotoImage(file=icon_path + 'grass.gif')
        self.icons['tree'] = PhotoImage(file=icon_path + 'tree.gif')
        self.icons['volcano'] = PhotoImage(file=icon_path + 'volcano.gif')
        self.icons['water'] = PhotoImage(file=icon_path + 'water.gif')
        self.icons['bridge'] = PhotoImage(file=icon_path + 'bridge.gif')
        self.icons['man'] = PhotoImage(file=icon_path + 'man.gif')
        self.icons['hive'] = PhotoImage(file=icon_path + 'hive.gif')

        # Make a board with all the features
        self.man = ['man', [[5, 0]]]
        self.set_cells(cells)
        self.grid_map = self.make_grid_map()
        self.set_features(features)

        # Generate a quit button
        self.quitButton = Button(self.frame, text='Quit', command=self.frame.quit)
        self.quitButton.grid(row=cells, column=cells // 2 + 1)
        self.boardButton = Button(self.frame, text='Board',
                                  command=lambda: self.board_command())
        self.boardButton.grid(row=cells, column=cells//2 - 1)
        self.startButton = Button(self.frame, text='Start',
                                  command=lambda: self.start_command())
        self.startButton.grid(row=cells, column=cells // 2)

    def get_cells(self):
        return self.cells

    def set_cells(self, new_cells):
        self.cells = new_cells

    def get_dimensions(self):
        return self.dimension

    def set_dimensions(self, new_dim):
        self.dimension = new_dim
        # Change the size of the frame

    def make_grid_map(self):
        cells = self.cells
        grid = []
        for i in range(cells):
            for j in range(cells):
                grid = grid + [[i, j]]
        return grid

    def get_features(self):
        return self.features

    def set_features(self, new_features):
        self.features = new_features
        self.generate_features()

    def generate_features(self):
        # Properties of features:
        # 1. identifier (barrier, lethal, unidirectional (bridge)
        # 2. location
        # NOTE: Fill in with grass, replace with other features

        # Get board properties
        cells = self.cells
        features = self.features

        # Separate ids and locations of specified features
        ids = features[0]
        locations = features[1]

        # Generate grass board
        for i in range(cells):
            for j in range(cells):
                label_name = 'label_' + str(i) + ',' + str(j)
                Label(self.frame, name=label_name, image=self.icons['grass'])
                widget_name = self.frame.widgetName + '.' + label_name
                self.frame.master.nametowidget(widget_name)\
                    .grid(row=i, column=j)

        # Replace with features
        for i in range(len(ids)):
            # Plot all features
            label_name = 'label_' + str(locations[i][0]) + ',' + str(locations[i][1])
            Label(self.frame, name=label_name, image=self.icons[ids[i]])
            widget_name = self.frame.widgetName + '.' + label_name
            self.frame.master.nametowidget(widget_name)\
                .grid(row=locations[i][0], column=locations[i][1])

        # Replace with man
        label_name = 'label_' + str(self.man[0][0]) + ',' + str(self.man[0][1])
        Label(self.frame, name=label_name, image=self.icons[self.man[0]])
        widget_name = self.frame.widgetName + '.' + label_name
        self.frame.master.nametowidget(widget_name) \
            .grid(row=self.man[1][0][0], column=self.man[1][0][1])

    def mouse_clicked(self):
        test = 1

    def key_pressed(self, event):

        if event.keysym in ('Right', 'Left', 'Up', 'Down'):
            print('Evaluated character is:', event.keysym)
            self.move_man(event.keysym)
        else:
            print('Use the arrow keys to move.')

    def move_man(self, direction):

        def check_swap():

            # Detect next man location feature
            # If it's a tree or water, don't go
            if new_man_loc in feat_locs:
                # Check for tree or water
                new_feat_index = feat_locs.index(new_man_loc)
                new_feat_id = feat_ids[new_feat_index]

                if not (new_feat_id == 'tree' or new_feat_id == 'water'):
                    # Can continue. Replace new location with man, replace old location with old feat.
                    swap_man()
            else:
                # Can continue
                swap_man()

        def swap_man():

            self.man[1][0] = new_man_loc

            # Detect prev man location original feature
            # If there's a feature there, replace it. If not, put grass there.
            if old_man_loc in feat_locs:
                # Replace the feature
                old_feat_index = feat_locs.index(old_man_loc)
                old_feat_name = feat_ids[old_feat_index]
            else:
                # Put grass there.
                old_feat_name = 'grass'

            label_name = 'label_' + str(old_man_loc[0]) + ',' + str(old_man_loc[1])
            Label(self.frame, name=label_name, image=self.icons[old_feat_name])
            widget_name = self.frame.widgetName + '.' + label_name
            self.frame.master.nametowidget(widget_name) \
                .grid(row=old_man_loc[0], column=old_man_loc[1])

            # Replace the new feature with man
            label_name = 'label_' + str(new_man_loc[0]) + ',' + str(new_man_loc[1])
            Label(self.frame, name=label_name, image=self.icons[self.man[0]])
            widget_name = self.frame.widgetName + '.' + label_name
            self.frame.master.nametowidget(widget_name) \
                .grid(row=new_man_loc[0], column=new_man_loc[1])

            check_win()

        def check_win():
            if 'hive' in feat_ids:
                hive_index = feat_ids.index('hive')
                if new_man_loc == feat_locs[hive_index]:
                    win_widget = Label(self.frame, name='win_widget', text='You Win!',
                                       font=('Arial', 30), justify=CENTER)
                    win_widget.place(x=self.frame.winfo_width(), y=self.frame.winfo_height())
                    root.update_idletasks()
                    win_widget.place(x=self.frame.winfo_width() // 2 - win_widget.winfo_width() // 2,
                                     y=self.frame.winfo_height() // 2 - win_widget.winfo_height() // 2)
                    root.update_idletasks()
                    root.after(5000, self.frame.quit())

        # Get features of current, next space
        # If feature is impenetrable, don't move
        # If it is, replace feature with man
        # Backfill with feature or grass

        feat_ids = self.features[0]
        feat_locs = self.features[1]
        man_loc = self.man[1][0]

        if direction == 'Right' and man_loc[1] < self.cells - 1:
            old_man_loc = man_loc[:]
            new_man_loc = [man_loc[0], man_loc[1] + 1]
            check_swap()
        elif direction == 'Left' and man_loc[1] > 0:
            old_man_loc = man_loc[:]
            new_man_loc = [man_loc[0], man_loc[1] - 1]
            check_swap()
        elif direction == 'Up' and man_loc[0] > 0:
            old_man_loc = man_loc[:]
            new_man_loc = [man_loc[0] - 1, man_loc[1]]
            check_swap()
        elif direction == 'Down' and man_loc[0] < self.cells - 1:
            old_man_loc = man_loc[:]
            new_man_loc = [man_loc[0] + 1, man_loc[1]]
            check_swap()

        test = 1

    def board_command(self):
        self.frame.unbind_all('<Key>')
        self.frame.bind_all('Button-1', self.mouse_clicked)
        test = 1

    def start_command(self):
        self.frame.unbind_all('Button-1')
        self.frame.bind_all('<Key>', self.key_pressed)

root = Tk()
root.title('Maze Game!')
root.resizable(0,0)

cells = 11
game_board = board(root, cells, [['hive', 'tree', 'tree'],
                              [[cells // 2, cells - 1], [0, 1], [5, 2]]])
# game_board.frame.bind('<Key>', game_board.keypress)
# game_board.frame.bind('<1>', game_board.keypress)

root.mainloop()

test = 1


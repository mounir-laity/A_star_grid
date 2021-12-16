from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import maze
from palettes import Palettes


class AStarApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.palette = Palettes.DEFAULT
        # https://coolors.co/e63946-f1faee-a8dadc-457b9d-1d3557
        # https://coolors.co/f4f1de-e07a5f-3d405b-81b29a-f2cc8f
        window_width = 600
        window_height = 325

        self.title("A* algorithm demonstration")
        self.iconbitmap("resources\icon.ico")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x_window = self.screen_width // 2 - window_width // 2
        y_window = self.screen_height // 2 - window_height // 2
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x_window, y_window))
        self.resizable(width=False, height=False)
        self.change_to_main_menu(self.palette)
        self.mainloop()

    def change_frame(self, new_frame):
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=BOTH, expand=True)

    def change_to_main_menu(self, palette: Palettes):
        new_frame = MainMenu(self, palette)
        self.change_frame(new_frame)

    def change_to_grid_window(self, palette: Palettes, rows, columns):
        padding = 100
        new_frame = GridWindow(self, palette, rows, columns)
        new_heigth = (rows + 2) * new_frame.pixel_width + padding
        new_width = (columns + 2) * new_frame.pixel_width
        x_window = self.screen_width // 2 - new_width // 2
        y_window = self.screen_height // 2 - new_heigth // 2
        self.geometry("%dx%d+%d+%d" % (new_width, new_heigth, x_window, y_window))
        self.change_frame(new_frame)

    def change_to_options_window(self, palette: Palettes):
        new_frame = OptionsWindow(self, self.palette)
        new_heigth = 325
        new_width = 600
        x_window = self.screen_width // 2 - new_width // 2
        y_window = self.screen_height // 2 - new_heigth // 2
        self.geometry("%dx%d+%d+%d" % (new_width, new_heigth, x_window, y_window))
        self.change_frame(new_frame)


class MainMenu(Frame):
    def __init__(self, parent: AStarApp, palette: Palettes):
        self.palette = palette
        FG_COLOR = palette.value[0]
        BG_COLOR = palette.value[1]
        Frame.__init__(self, parent, background=palette.value[1])
        title_label = Label(
            self,
            text="A* ALGORITHM DEMONSTRATION",
            font=("Courrier", 24),
            bg=BG_COLOR,
            fg=FG_COLOR,
        )

        size_label = Label(
            self,
            text="Please enter the size of the grid :",
            font=("Courrier", 15),
            bg=BG_COLOR,
            fg=FG_COLOR,
        )

        height_label = Label(
            self,
            text="Height : ",
            font=("Courrier", 15),
            bg=BG_COLOR,
            fg=FG_COLOR,
        )

        width_label = Label(
            self,
            text="Width : ",
            font=("Courrier", 15),
            bg=BG_COLOR,
            fg=FG_COLOR,
        )

        value_list = [i for i in range(10, 41)]
        height_box = Combobox(
            self,
            values=value_list,
            width=5,
            height=20,
            state="readonly",
            font=("Courrier", 15),
        )
        height_box.current(0)

        width_box = Combobox(
            self,
            values=value_list,
            width=5,
            height=20,
            state="readonly",
            font=("Courrier", 15),
        )
        width_box.current(0)

        launch_button = Button(
            self,
            text="Launch",
            font=("Courrier", 15),
            bg=BG_COLOR,
            fg=FG_COLOR,
            command=lambda: parent.change_to_grid_window(
                self.palette, int(height_box.get()), int(width_box.get())
            ),
        )

        options_button = Button(
            self,
            text="Options",
            font=("Courrier", 15),
            bg=BG_COLOR,
            fg=FG_COLOR,
            command=lambda: parent.change_to_options_window(self.palette),
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        title_label.grid(row=0, column=0, pady=10, columnspan=3)
        size_label.grid(row=1, column=0, pady=10, ipadx=10, ipady=5, columnspan=2)
        height_label.grid(row=2, column=0, sticky=E)
        height_box.grid(row=2, column=1, sticky=W)
        width_label.grid(row=3, column=0, sticky=E)
        width_box.grid(row=3, column=1, sticky=W)
        launch_button.grid(row=4, column=0, pady=10, ipadx=10, ipady=5, columnspan=3)
        options_button.grid(row=5, column=0, pady=10, ipadx=10, ipady=5, columnspan=3)


class GridWindow(Frame):
    def __init__(self, parent: AStarApp, palette: Palettes, rows, columns):
        self.pixel_width = 20
        self.rect_ids = []
        self.palette = palette
        self.FG_COLOR = palette.value[0]
        self.BG_COLOR = palette.value[1]
        self.WALL_COLOR = palette.value[2]
        self.START_COLOR = palette.value[3]
        self.DEST_COLOR = palette.value[4]
        self.PATH_COLOR = palette.value[5]
        self.EXPLORED_COLOR = palette.value[6]

        self.rows = rows
        self.columns = columns
        self.erase_mode = False
        self.has_start = False
        self.has_dest = False
        self.generated = False
        self.allow_diagonal = BooleanVar()
        self.allow_diagonal.set(False)

        Frame.__init__(
            self,
            parent,
            background=self.BG_COLOR,
            height=(rows + 2) * self.pixel_width,
            width=(columns + 2) * self.pixel_width,
        )
        self.canvas = Canvas(self, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        self.gen_button = Button(
            self,
            text="Find path",
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            command=self.launch,
        )
        self.restart_button = Button(
            self,
            text="Restart",
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            command=self.restart,
        )
        self.diagonal_checkbutton = Checkbutton(
            self,
            text="Allow diagonal movement",
            font=("Courrier", 13),
            var=self.allow_diagonal,
            onvalue=True,
            offvalue=False,
            bg=self.BG_COLOR,
        )

        self.canvas.grid(
            row=0, column=0, padx=self.pixel_width, pady=self.pixel_width, columnspan=3
        )
        self.canvas.config(
            height=rows * self.pixel_width + 1, width=columns * self.pixel_width + 1
        )
        self.create_grid(rows, columns)
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-3>", self.handle_right_click)
        self.canvas.bind("<Button-2>", self.clear_grid)

        self.gen_button.grid(row=1, column=0, padx=10, pady=5)
        self.restart_button.grid(row=1, column=2, padx=10, pady=5)
        self.diagonal_checkbutton.grid(row=2, column=0, padx=10, pady=5, columnspan=3)

    def create_grid(self, rows, columns):
        for y in range(rows):
            for x in range(columns):
                x1 = x * self.pixel_width
                x2 = x1 + self.pixel_width
                y1 = y * self.pixel_width
                y2 = y1 + self.pixel_width
                self.rect_ids.append(self.canvas.create_rectangle(x1, y1, x2, y2))
        for rect in self.rect_ids:
            self.canvas.itemconfig(rect, fill=self.BG_COLOR)

    def get_clicked_square(self, x, y):
        width = self.pixel_width
        if x >= 0 and y >= 0 and x < self.columns * width and y < self.rows * width:
            return (x // width) + 1 + self.columns * (y // width)
        return -1

    def handle_left_click(self, event):
        if not self.generated:
            rect_id = self.get_clicked_square(event.x, event.y)
            if rect_id != -1:
                color = self.canvas.itemcget(rect_id, "fill")
                if color == self.BG_COLOR:
                    self.canvas.itemconfig(rect_id, fill=self.WALL_COLOR)
                    self.erase_mode = False
                elif color == self.WALL_COLOR:
                    self.canvas.itemconfig(rect_id, fill=self.BG_COLOR)
                    self.erase_mode = True

    def draw(self, event):
        if not self.generated:
            rect_id = self.get_clicked_square(event.x, event.y)
            if rect_id != -1:
                color = self.canvas.itemcget(rect_id, "fill")
                if not self.erase_mode:
                    if color == self.BG_COLOR:
                        self.canvas.itemconfig(rect_id, fill=self.WALL_COLOR)
                else:
                    if color != self.START_COLOR and color != self.DEST_COLOR:
                        self.canvas.itemconfig(rect_id, fill=self.BG_COLOR)

    def handle_right_click(self, event):
        if not self.generated:
            rect_id = self.get_clicked_square(event.x, event.y)
            if rect_id != -1:
                color = self.canvas.itemcget(rect_id, "fill")
                if color == self.BG_COLOR:
                    if not self.has_start:
                        self.has_start = True
                        self.canvas.itemconfig(rect_id, fill=self.START_COLOR)
                    elif not self.has_dest:
                        self.has_dest = True
                        self.canvas.itemconfig(rect_id, fill=self.DEST_COLOR)
                elif color == self.START_COLOR:
                    self.canvas.itemconfig(rect_id, fill=self.BG_COLOR)
                    self.has_start = False
                elif color == self.DEST_COLOR:
                    self.canvas.itemconfig(rect_id, fill=self.BG_COLOR)
                    self.has_dest = False

    def clear_grid(self, event):
        if not self.generated:
            for rect in self.rect_ids:
                self.canvas.itemconfig(rect, fill=self.BG_COLOR)
            self.has_dest = False
            self.has_start = False

    def get_id_from_position(self, position: tuple[int, int]):
        row = position[0]
        column = position[1]
        return row * self.columns + (column + 1)

    def convert_to_graph(self):
        graph = maze.Graph(self.rows, self.columns)
        for rect in self.rect_ids:
            node_row = (rect - 1) // self.columns
            node_column = (rect - 1) % self.columns
            color = self.canvas.itemcget(rect, "fill")
            if color == self.WALL_COLOR:
                graph.add_wall(node_row, node_column)
            elif color == self.START_COLOR:
                graph.set_start_node(node_row, node_column)
            elif color == self.DEST_COLOR:
                graph.set_end_node(node_row, node_column)
        return graph

    def launch(self):
        if not self.generated and self.has_start and self.has_dest:
            self.generated = True
            path_color = self.PATH_COLOR
            explored_color = self.EXPLORED_COLOR
            self.convert_to_graph()
            graph = self.convert_to_graph()
            path, explored = graph.a_star_algo(self.allow_diagonal.get())
            for node in explored:
                rect_id = self.get_id_from_position(node.position)
                self.canvas.itemconfig(rect_id, fill=explored_color)
            if path is not None:
                for position in path:
                    rect_id = self.get_id_from_position(position)
                    self.canvas.itemconfig(rect_id, fill=path_color)

            else:
                alert_box = messagebox.showinfo(
                    "No path found !", "There is no path to the destination !"
                )

    def restart(self):
        self.generated = False
        self.clear_grid(None)


class OptionsWindow(Frame):
    def __init__(self, parent: AStarApp, palette: Palettes):
        self.palette = palette
        self.FG_COLOR = palette.value[0]
        self.BG_COLOR = palette.value[1]
        self.list_components = []
        Frame.__init__(self, parent, background=palette.value[1])

        palette_selection_label = Label(
            self,
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            text="Select your color palette :",
        )
        self.list_components.append(palette_selection_label)
        values_list = []
        for e in Palettes:
            values_list.append(e.name.replace("_", " ").capitalize())
        palette_selection_box = Combobox(
            self,
            values=values_list,
            width=12,
            height=10,
            state="readonly",
            font=("Courrier", 15),
        )
        palette_selection_box.current(0)
        palette_selection_box.bind(
            "<<ComboboxSelected>>",
            lambda _: self.select_color_palette(palette_selection_box.get()),
        )
        self.list_components.append(palette_selection_box)

        back_to_menu_button = Button(
            self,
            text="Back to menu",
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            command=lambda: parent.change_to_main_menu(self.palette),
        )
        self.list_components.append(back_to_menu_button)

        self.grid_columnconfigure(0, weight=1)
        palette_selection_label.grid(row=0, column=0, pady=10, ipady=10)
        palette_selection_box.grid(row=1, column=0, pady=10, ipady=10)
        back_to_menu_button.grid(row=2, column=0, pady=10, ipady=10)

    def change_color_palette(self, palette_name: str):
        palette_name = palette_name.upper().replace(" ", "_")
        self.palette = Palettes[palette_name]
        self.FG_COLOR = self.palette.value[0]
        self.BG_COLOR = self.palette.value[1]
        self.config(bg=self.BG_COLOR)

    def update_components(self):
        for component in self.list_components:
            component.configure(background=self.BG_COLOR)

    def select_color_palette(self, palette_name: str):
        self.change_color_palette(palette_name)
        self.update_components()


if __name__ == "__main__":
    app = AStarApp()
    app.mainloop()

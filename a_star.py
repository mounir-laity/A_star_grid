from tkinter import *
from tkinter import messagebox
import tkinter
from tkinter.ttk import Combobox
import maze
from palettes import Palettes
import os
import sys


class AStarApp(Tk):
    """This application uses the A star algorithm to find the shortest path between two
    squares in a grid. It uses tkinter for the GUI.
    """

    def __init__(self) -> None:
        """Creates a new window of adequate size and launches the main menu of the application.

        Attributes:
            palette (Palettes): The current color palette of the application.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
        """
        Tk.__init__(self)
        self._frame = None
        self.palette = Palettes.DEFAULT
        window_width = 600
        window_height = 325
        self.title("A* algorithm")
        try:
            self.iconbitmap("resources\icon.ico")  # comment this line for pyinstaller
        except tkinter.TclError:
            pass
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x_window = self.screen_width // 2 - window_width // 2
        y_window = self.screen_height // 2 - window_height // 2
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x_window, y_window))
        self.resizable(width=False, height=False)
        self.change_to_main_menu(self.palette)
        self.mainloop()

    def change_frame(self, new_frame: Frame) -> None:
        """Destroys the current frame and switches to the new frame

        Args:
            new_frame (Frame): The new frame to display
        """
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=BOTH, expand=True)

    def change_to_main_menu(self, palette: Palettes) -> None:
        """Displays the main menu frame.

        Args:
            palette (Palettes): The color palette to apply.
        """
        new_frame = MainMenu(self, palette)
        self.change_frame(new_frame)
        self.title("A* algorithm - Main Menu")

    def change_to_grid_window(self, palette: Palettes, rows: int, columns: int) -> None:
        """Changes the frame to the grid window frame.

        Args:
            palette (Palettes): The color palette to apply.
            rows (int): The number of rows of the grid.
            columns (int): The number of columns of the grid.
        """
        padding = 100
        new_frame = GridWindow(self, palette, rows, columns)
        new_heigth = (rows + 2) * new_frame.square_width + padding
        new_width = (columns + 2) * new_frame.square_width
        x_window = self.screen_width // 2 - new_width // 2
        y_window = self.screen_height // 2 - new_heigth // 2
        self.geometry("%dx%d+%d+%d" % (new_width, new_heigth, x_window, y_window))
        self.change_frame(new_frame)
        self.title("A* algorithm")

    def change_to_options_window(self, palette: Palettes) -> None:
        """Changes the frame to display the options window.

        Args:
            palette (Palettes): The color palette to apply.
        """
        new_frame = OptionsWindow(self, palette)
        new_heigth = 325
        new_width = 600
        x_window = self.screen_width // 2 - new_width // 2
        y_window = self.screen_height // 2 - new_heigth // 2
        self.geometry("%dx%d+%d+%d" % (new_width, new_heigth, x_window, y_window))
        self.change_frame(new_frame)
        self.title("A* algorithm - Options Menu")


class MainMenu(Frame):
    """This represents the main menu of the application.
    It allows the user to choose the size of the grid and to go to the options menu.
    """

    def __init__(self, parent: AStarApp, palette: Palettes) -> None:
        """Creates a main menu frame for the application.

        Attributes:
            palette (Palettes): The current color palette of the main menu.

        Args:
            parent (AStarApp): The application using the frame.
            palette (Palettes): The color palette to apply.
        """
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
    """This represents the grid window of the application.
    In this window, the user can set the maze up for the a star algorithm.
    They can put the start and goal squares and draw walls. They can also
    choose whether to allow diagonal movement for the algorithm. It also allows
    the user to try with multiple configurations simply by restarting the grid.
    """

    def __init__(
        self, parent: AStarApp, palette: Palettes, rows: int, columns: int
    ) -> None:
        """Creates a grid frame for the application.

        Attributes:
            square_width (int): The width of a square of the grid.
            rect_ids (list[int]): The list of all ids of  the squares contained in the grid.
            palette (Palettes): The color palette to apply.
            FG_COLOR (str): The value for the foreground color of the window.
            BG_COLOR (str): The value for the background color of the window.
            WALL_COLOR (str): The value for the wall color of the window.
            START_COLOR (str): The value for the starting square color of the window.
            DEST_COLOR (str): The value for the goal square color of the window.
            PATH_COLOR (str): The value for the path color of the window.
            EXPLORED_COLOR (str): The value for the explored squares color of the window.
            rows (int): The number of rows in the grid.
            columns (int): The number of columns in the grid.
            erase_mode (bool): Determines if the left click should erase walls or not.
            has_start (bool): Determines if there is a starting square for the algorithm.
            has_dest (bool): Determines if there is a goal square for the algorithm.
            generated (bool): Determines if the algorithm has generated a path or not.
            allow_diagonal (bool): Determines if diagonal movement is allowed by the algorithm.
            canvas (Canvas): The canvas where the grid is drawn.

        Args:
            parent (AStarApp): The application using this frame.
            palette (Palettes): The color palette to apply.
            rows (int): The number of rows for the grid.
            columns (int): The number of columns for the grid.
        """
        self.square_width = 20
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
            height=(rows + 2) * self.square_width,
            width=(columns + 2) * self.square_width,
        )
        self.canvas = Canvas(self, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        gen_button = Button(
            self,
            text="Find path",
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            command=self.launch,
        )
        restart_button = Button(
            self,
            text="Restart",
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            command=self.restart,
        )
        diagonal_checkbutton = Checkbutton(
            self,
            text="Allow diagonal movement",
            font=("Courrier", 13),
            var=self.allow_diagonal,
            onvalue=True,
            offvalue=False,
            bg=self.BG_COLOR,
        )

        self.canvas.grid(
            row=0,
            column=0,
            padx=self.square_width,
            pady=self.square_width,
            columnspan=3,
        )
        self.canvas.config(
            height=rows * self.square_width + 1, width=columns * self.square_width + 1
        )
        self.create_grid(rows, columns)
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-3>", self.handle_right_click)
        self.canvas.bind("<Button-2>", self.clear_grid)

        gen_button.grid(row=1, column=0, padx=10, pady=5)
        restart_button.grid(row=1, column=2, padx=10, pady=5)
        diagonal_checkbutton.grid(row=2, column=0, padx=10, pady=5, columnspan=3)

    def create_grid(self, rows: int, columns: int) -> None:
        """Creates a grid in the canvas based on the desired dimensions and adds the created
        squares to rect_ids.

        Args:
            rows (int): The number of rows of the grid.
            columns (int): The number of columns of the grid.
        """
        for y in range(rows):
            for x in range(columns):
                x1 = x * self.square_width
                x2 = x1 + self.square_width
                y1 = y * self.square_width
                y2 = y1 + self.square_width
                self.rect_ids.append(self.canvas.create_rectangle(x1, y1, x2, y2))
        for rect in self.rect_ids:
            self.canvas.itemconfig(rect, fill=self.BG_COLOR)

    def get_clicked_square(self, x: int, y: int) -> int:
        """Gets the id of the square based on the position of the cursor when the click occured.

        Args:
            x (int): The x-axis of the cursor when the click occured.
            y (int): The y-axis of the cursor when the click occured.

        Returns:
            int: The id of the clicked square.
        """
        width = self.square_width
        if x >= 0 and y >= 0 and x < self.columns * width and y < self.rows * width:
            return (x // width) + 1 + self.columns * (y // width)
        return -1

    def handle_left_click(self, event: Event) -> None:
        """Makes the square at the cursor's position a wall when a left click event
        is recognized. It will erase the wall instead if it is already a wall.

        Args:
            event (Event): The left click event.
        """
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

    def draw(self, event: Event) -> None:
        """Draws wall on all squares hovered by the cursor while the left click button is
        held down.
        If the first square hovered is a wall, it will instead erase all walls hovered by
        the cursor while the left click button is held down.

        Args:
            event (Event): The left click holding event.
        """
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

    def handle_right_click(self, event: Event) -> None:
        """Creates a starting square on the square at the cursor's position
        if it isn't already existing. If it is here, it will create a goal square
        on the square at the cursor's position if it isn't already existing.
        If the square is already a starting or goal square, it will remove it instead.

        Args:
            event (Event): The right click event.
        """
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

    def clear_grid(self, event: Event):
        """Clears the grid by removing all walls, the start and the end squares.

        Args:
            event (Event): The middle mouse button event.
        """
        if not self.generated:
            for rect in self.rect_ids:
                self.canvas.itemconfig(rect, fill=self.BG_COLOR)
            self.has_dest = False
            self.has_start = False

    def get_id_from_position(self, position: tuple[int, int]) -> int:
        """Gets the rectangle id corresponding of the square at the given position.

        Args:
            position (tuple[int, int]): The position to get the square id from.

        Returns:
            int: The id of the square at the position.
        """
        row = position[0]
        column = position[1]
        return row * self.columns + (column + 1)

    def convert_to_graph(self) -> maze.Graph:
        """Converts the grid of squares to a Graph of Nodes.

        Returns:
            maze.Graph: The Graph obtained by converting the grid.
        """
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
                graph.set_dest_node(node_row, node_column)
        return graph

    def launch(self) -> None:
        """Uses the a star algorithm to find the shortest path between the start and destination.
        The path will be showed in its own color and all explored squares are also shown.
        If there is no path possible between the two Nodes, a message box appears to inform the user.
        """
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

    def restart(self) -> None:
        """Clears the grid and allows the user to start drawing again."""
        self.generated = False
        self.clear_grid(None)


class OptionsWindow(Frame):
    """This class represents the options window where the user
    can change color palettes for the application.
    """

    def __init__(
        self,
        parent: AStarApp,
        palette: Palettes,
    ) -> None:
        """Creates an optionsWindow frame for the application.

        Attributes:
            palette (Palettes): The color palette for this frame.
            FG_COLOR (str): The foreground color of this frame.
            BG_COLOR (str): The background color of this frame.
            list_components (list): The list of all widgets of this frame.

        Args:
            parent (AStarApp): The parent application using this frame.
            palette (Palettes): The color palette to apply.
        """
        self.palette = palette
        self.FG_COLOR = palette.value[0]
        self.BG_COLOR = palette.value[1]
        self.list_components = []
        Frame.__init__(self, parent, background=palette.value[1])

        usage_label = Label(
            self,
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            text="Usage:\n"
            + "Left click: Draw/erase walls\n"
            + "Right click: Set starting square and goal square\n"
            + "Middle click: Clear grid",
        )
        self.list_components.append(usage_label)

        palette_selection_label = Label(
            self,
            font=("Courrier", 15),
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            text="Color palette :",
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
        palette_selection_box.current(self.palette.value[7])
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
        usage_label.grid(row=0, column=0, pady=5, ipady=10)
        palette_selection_label.grid(row=1, column=0, pady=5, ipady=10)
        palette_selection_box.grid(row=2, column=0, pady=5, ipady=10)
        back_to_menu_button.grid(row=3, column=0, pady=5, ipady=10)

    def change_color_palette(self, palette_name: str) -> None:
        """Changes the color palette and applies the new one.

        Args:
            palette_name (str): The new color palette name to change to.
        """
        palette_name = palette_name.upper().replace(" ", "_")
        self.palette = Palettes[palette_name]
        self.FG_COLOR = self.palette.value[0]
        self.BG_COLOR = self.palette.value[1]
        self.config(bg=self.BG_COLOR)

    def update_components(self) -> None:
        """Updates the foreground and background colors of all widgets."""
        for component in self.list_components:
            component.config(background=self.BG_COLOR)
            component.config(foreground=self.FG_COLOR)

    def select_color_palette(self, palette_name: str) -> None:
        """Applies the chosen color palette.

        Args:
            palette_name (str): The name of the color palette to apply.
        """
        self.change_color_palette(palette_name)
        self.update_components()


if __name__ == "__main__":
    """Launches the application"""
    app = AStarApp()
    app.mainloop()

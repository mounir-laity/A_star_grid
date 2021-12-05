from tkinter import *
from tkinter.ttk import Combobox
from typing import List


class AStarApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        window_width = 600
        window_height = 300
        BG_COLOR = "#8B2635"
        FG_COLOR = "#D2D4C8"

        self.title("A* algorithm demonstration")
        self.iconbitmap("resources\icon.ico")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x_window = self.screen_width // 2 - window_width // 2
        y_window = self.screen_height // 2 - window_height // 2
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x_window, y_window))
        self.resizable(width=False, height=False)
        self.change_to_main_menu(BG_COLOR, FG_COLOR)
        self.mainloop()

    def change_frame(self, new_frame):
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=BOTH, expand=True)

    def change_to_main_menu(self, BG_COLOR, FG_COLOR):
        new_frame = MainMenu(self, BG_COLOR, FG_COLOR)
        self.change_frame(new_frame)

    def change_to_grid_window(self, BG_COLOR, FG_COLOR, rows, columns):
        new_frame = GridWindow(self, BG_COLOR, FG_COLOR, rows, columns)
        new_heigth = (rows + 2) * new_frame.pixel_width + 60
        new_width = (columns + 2) * new_frame.pixel_width
        x_window = self.screen_width // 2 - new_width // 2
        y_window = self.screen_height // 2 - new_heigth // 2
        self.geometry("%dx%d+%d+%d" % (new_width, new_heigth, x_window, y_window))
        self.change_frame(new_frame)


class MainMenu(Frame):
    def __init__(self, parent: AStarApp, BG_COLOR, FG_COLOR):
        Frame.__init__(self, parent, background=BG_COLOR)
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
                BG_COLOR, FG_COLOR, int(height_box.get()), int(width_box.get())
            ),
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        title_label.grid(row=0, column=0, pady=10, columnspan=3)
        size_label.grid(row=4, column=0, pady=10, ipadx=10, ipady=5, columnspan=2)
        height_label.grid(row=5, column=0, sticky=E)
        height_box.grid(row=5, column=1, sticky=W)
        width_label.grid(row=6, column=0, sticky=E)
        width_box.grid(row=6, column=1, sticky=W)
        launch_button.grid(row=7, column=0, pady=20, ipadx=10, ipady=5, columnspan=3)


class GridWindow(Frame):
    def __init__(self, parent: AStarApp, BG_COLOR, FG_COLOR, rows, columns):
        self.pixel_width = 20
        self.rect_ids = []

        self.BG_COLOR = BG_COLOR
        self.FG_COLOR = FG_COLOR
        self.WALL_COLOR = "#2E3532"
        self.START_COLOR = "#E0E2DB"
        self.DEST_COLOR = "#D3EFBD"

        self.rows = rows
        self.columns = columns
        self.erase_mode = False
        self.has_start = False
        self.has_dest = False

        Frame.__init__(
            self,
            parent,
            background=BG_COLOR,
            height=(rows + 2) * self.pixel_width,
            width=(columns + 2) * self.pixel_width,
        )
        self.canvas = Canvas(self, bg=BG_COLOR, bd=0, highlightthickness=0)
        self.gen_button = Button(
            self,
            text="Generate",
            font=("Courrier", 15),
            bg=BG_COLOR,
            fg=FG_COLOR,
            command=self.launch,
        )

        self.canvas.grid(row=0, column=0, padx=self.pixel_width, pady=self.pixel_width)
        self.canvas.config(
            height=rows * self.pixel_width + 1, width=columns * self.pixel_width + 1
        )
        self.create_grid(rows, columns)
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-3>", self.handle_right_click)
        self.canvas.bind("<Button-2>", self.clear_grid)

        self.gen_button.grid(row=1, column=0)

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
        for rect in self.rect_ids:
            self.canvas.itemconfig(rect, fill=self.BG_COLOR)
        self.has_dest = False
        self.has_start = False

    def launch(self):
        print("launching !")


class Level:
    def __init__(self, rows, columns) -> None:
        my_list = list(range(1, (rows * columns) + 1))


if __name__ == "__main__":
    level = Level(10, 10)
    app = AStarApp()
    app.mainloop()


# A star algorithm demonstration with Tkinter

This project is a gui visualisation of the A star algorithm using Tkinter. It allows you to create a maze for the algorithm to find the shortest path between two points.

## How to run
All you have to do is run the command : 

    python3 a_star.py
This project only uses Tkinter. Since Tkinter is already included in the Python 3 standard library, you don't even need to install anything !

## How to use
### Main Menu
When launching this program, you'll be greeted with the main menu where you can choose the grid's size, go to the options menu or create the grid.
![This is the first window that opens when launching the application](https://imageshack.com/i/pmnofL1vp)The size of the grid can go from 10x10 to 40x40.
### Options window
This is the options window of the application. It allows you to see the controls and it allows you to change the color palette. Right now, there are 3 differents color palettes but more may be added in the future. You can also add them yourself by adding a new value in the *Palettes* enum if you want.
![You can change the color palette here](https://imageshack.com/i/pnVo7qo2p)
### Grid window
This is the main window. You can create your maze here. The left mouse button allows you to draw/erase walls. You can setup a starting and goal position with the right click button. The middle mouse button lets you clear the grid. You can also decide whether to authorise diagonal movement or not. When you have everything setup, you can click on the ***Find path*** button to let the algorithm find the shortest path between you starting square and goal square.
![Left click to draw walls, right click for start and goal squares](https://imageshack.com/i/poJmq12Og)

## Pyinstaller
To create an executable for this project using pyinstaller, i recommand **[using auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/)**
For that, you'll need to comment the requested line line in the *a_star.py* file (just search for "pyinstaller" in the file) since tkinter's *iconbitmap* method doesn't work great with pyinstaller.

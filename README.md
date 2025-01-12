# Draw++ Project - Drawing Language



# Project Description

Draw++ is a simple and intuitive language designed specifically for drawing. It allows users to create geometric shapes like circles, rectangles, or squares by writing specific commands. These commands can include parameters such as position, color, or shape thickness. To enhance usability, an interactive editor has been developed. This editor can analyze, correct, and execute commands in real time, offering a smooth and user-friendly experience.



# Launch Instructions

Install Required Dependencies:

tkinter (for the graphical interface) :
`sudo apt update`
`sudo apt install python3-tk -y`

gcc (for compiling the C code) :
`sudo apt update`
`sudo apt install build-essential`

SDL2 library (for graphics rendering) :
`sudo apt-get update`
`sudo apt-get install libsdl2-dev`

Start the Program :

`python3 main.py`


# Key Features

# Basic Commands : 

Create Cursor: create_cursor(name, x, y) – Creates a cursor at position (x, y).

Move Cursor: move_cursor(name, x, y) – Moves a cursor to position (x, y).

Show/Hide Cursor: show_cursor(name) or hide_cursor(name) – Makes a cursor visible or hides it.

Rotate Cursor: rotate_cursor(name, angle) – Rotates the cursor by angle degrees.

Set Thickness: thickness_cursor(name, thickness) – Sets the line thickness for the cursor.

Set Color: color_cursor(name, r, g, b) – Sets the color (r, g, b) for the cursor.

# Drawing Commands : 

Draw Line: draw_line(name, length) – Draws a line of specified length.

Draw Rectangle: draw_rectangle(name, width, height) – Draws a rectangle with given width and height.

Draw Square: draw_square(name, size) – Draws a square with sides of size.

Draw Circle: draw_circle(name, radius) – Draws a circle with a specified radius.

Draw Ellipse: draw_ellipse(name, width, height) – Draws an ellipse with given width and height.

Draw Arc: draw_arc(name, radius, start_angle, end_angle) – Draws an arc with a given radius and angles.

Draw Star: draw_star(name, branches, size) – Draws a star with a specified number of branches and size.

# Advanced Commands : 

Variables: var name = value – Assigns a value to a variable.

Conditionals: if, else – Allows conditional execution of commands.

Loops: repeat(n) – Repeats a block of instructions n times.

Functions: Custom blocks of reusable commands.
    

# Integrated IDE

The Draw++ Integrated Development Environment (IDE) is a powerful, user-friendly tool that simplifies the process of creating, editing, and running Draw++ programs. Its features include:


Tabbed File Management:

Open, create, and manage multiple files in separate tabs.
Rename tabs for better organization.
Autosave and manual save options ensure your work is not lost.


Real-Time Syntax Highlighting:

Highlights commands, conditionals, loops, functions, and variables with distinct colors.
Provides instant feedback on errors with red underlines.


Interactive Command Validation:

Validates syntax as you type, marking valid and invalid lines.
Detects missing parameters or incorrect command usage.


Code Execution:

Runs your Draw++ code and displays the results in a graphical window.
Supports real-time rendering of shapes, lines, and other elements.


Undo/Redo Functionality:

Easily revert or reapply changes to your code.


Dark and Light Modes:

Toggle between dark mode for comfortable nighttime use and light mode for daytime.


Error Management:

Errors in your code are highlighted for quick fixes.


Interactive Documentation:

Access built-in documentation directly from the IDE, providing explanations and examples of all commands.


Auto-completion:

Predicts and completes commands as you type, speeding up coding and reducing errors.



# Documentation

A detailed syntax guide is available in /syntax.txt. It includes a complete description of the language's commands, syntax, and usage examples.




# Development Team

YAZIDI Asma ; 
EL KHARROUBI Rayan ; 
MEGNOUX Julien ; 
MEDDOUR Bissem ;
SMAILI Adel ;





# Aide : Pour deposer des modifications depuis un depot local :
1. Avant le `add` toujours faire un `git pull` pour ne pas écraser le travail des autres.
2. `git add .`
3. `git commit -m "Message décrivant les modifications"`
4. Avant le `git push origin main`, toujours faire validé ces modifs en testant et par l'équipe.
5. `git push origin main`





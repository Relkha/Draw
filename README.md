# Draw++ Project - Drawing Language



# Project Description

Draw++ est un langage simple et intuitif conçu spécialement pour le dessin. Grâce à lui, il est possible de créer des formes géométriques comme des cercles, des rectangles ou des carrés en écrivant des commandes spécifiques. Ces commandes permettent aussi d’ajouter des paramètres tels que la position, la couleur ou l’épaisseur des formes. Pour faciliter son utilisation, un éditeur interactif a été développé. Cet éditeur est capable d’analyser, de corriger et d’exécuter les commandes en temps réel, offrant ainsi une expérience fluide et accessible.

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
    

# IDE Intégré 
- Création et gestion de fichiers Draw++.
- Exécution de programmes avec gestion des erreurs.
- Outils pour zoomer, déplacer, et modifier des dessins.


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





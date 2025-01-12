import tkinter as tk
from tkinter import ttk


def open_documentation_window():
    """
    Function to open an interactive documentation window.
    """
    # Create a new window
    doc_window = tk.Toplevel()
    doc_window.title("Interactive Documentation - Draw++")
    doc_window.geometry("600x500")

    # Create a main frame to hold everything
    main_frame = ttk.Frame(doc_window)
    main_frame.pack(fill="both", expand=True)

    # Add a canvas for scrolling
    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Add a frame inside the canvas
    content_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Add a search bar
    search_frame = ttk.Frame(content_frame)
    search_frame.pack(fill="x", padx=10, pady=5)

    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side="left")

    search_entry = ttk.Entry(search_frame, width=40)
    search_entry.pack(side="left", padx=5)

    def perform_search():
        query = search_entry.get().lower()
        for child in notebook.winfo_children():
            for widget in child.winfo_children():
                if isinstance(widget, tk.Label):
                    if query in widget.cget("text").lower():
                        notebook.select(child)
                        widget.focus()
                        return
        tk.messagebox.showinfo("Result", "No results found for: " + query)

    search_button = ttk.Button(search_frame, text="Search", command=perform_search)
    search_button.pack(side="left")

    # Create a Notebook widget to organize sections
    notebook = ttk.Notebook(content_frame)
    notebook.pack(expand=True, fill="both")
    
    # General section
    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="General")
    
    general_label = tk.Label(general_frame, 
        text="Welcome to Draw++!\n\n"
             "Draw++ is a simple language dedicated to geometric drawing.\n"
             "Use specific commands to create shapes, "
             "control cursors, and much more.\n\n"
             "The categories of instructions are:\n"
             "- Simple commands\n"
             "- Variable or instruction of assignation (var)\n"
             "- Function (def)\n"
             "- Conditional instructions (if...else)\n"
             "- Loops (repeat)\n\n"
             "Note: The drawing window size is fixed at 800x600.\n\n"
             "Warning: Ensure all commands follow the correct syntax to avoid errors.",
        justify="left", wraplength=550)
    general_label.pack(padx=10, pady=10)
    
   # Section for simple commands
    commands_frame = ttk.Frame(notebook)
    notebook.add(commands_frame, text="Simple Commands")

    commands_label = tk.Label(commands_frame, 
        text="Examples of simple commands:\n\n"
             "1. Create a cursor:\n"
             "   create_cursor -> create_cursor C (x,y)\n"
             "      example: create_cursor C1 (150,100)\n"
             "      (Create a cursor named C1 at the point with x=150 and y=100)\n\n"
             "2. Show a cursor:\n"
             "   show_cursor -> show_cursor C (by default, the cursor is visible)\n"
             "      example: show_cursor C1\n"
             "      (Show the cursor C1)\n\n"
             "3. Hide a cursor:\n"
             "   hide_cursor -> hide_cursor C\n"
             "      example: hide_cursor C1\n"
             "      (Hide the cursor C1)\n\n"
             "4. Move a cursor (jump):\n"
             "   move_cursor -> move_cursor C (x,y)\n"
             "      example: move_cursor C1 (100,150)\n"
             "      (Move the cursor C1 to the point with x=100 and y=150)\n\n"
             "5. Rotate a cursor:\n"
             "   rotate_cursor -> rotate_cursor C x (default: the cursor points up and rotates to the right)\n"
             "      example: rotate_cursor C1 90\n"
             "      (Rotate the cursor C1 by 90 degrees)\n\n"
             "6. Change the cursor color:\n"
             "   color_cursor -> color_cursor C (R,G,B)\n"
             "      example: color_cursor C1 (255,0,0)\n"
             "      (Change the color of cursor C1 to red)\n\n"
             "7. Change the cursor thickness:\n"
             "   thickness_cursor -> thickness_cursor C (1, 2, 3, 4, or 5) (predefined thickness levels)\n"
             "      example: thickness_cursor C1 4\n"
             "      (Change the thickness of cursor C1 to level 4)\n\n"
             "8. Draw a line:\n"
             "   draw_line -> draw_line C x\n"
             "      example: draw_line C1 20\n"
             "      (From the cursor C1, draw a line of 20 pixels)\n\n"
             "9. Draw a rectangle:\n"
             "   draw_rectangle -> draw_rectangle C x,y (by default, corners are drawn to the right)\n"
             "      example: draw_rectangle C1 (20,15)\n"
             "      (From the cursor C1, draw a rectangle 20 pixels long and 15 pixels wide)\n\n"
             "10. Draw a square:\n"
             "    draw_square -> draw_square C x (by default, corners are drawn to the right)\n"
             "      example: draw_square C1 20\n"
             "      (From the cursor C1, draw a square with a side length of 20 pixels)\n\n"
             "11. Draw a circle:\n"
             "    draw_circle -> draw_circle C x\n"
             "      example: draw_circle C1 20\n"
             "      (From the cursor C1, draw a circle with a radius of 20 pixels)\n\n"
             "12. Draw an arc:\n"
             "    draw_arc -> draw_arc C R a b\n"
             "      example: draw_arc C1 15 60 90\n"
             "      (From the cursor C1, draw an arc with a radius of 15 pixels, starting at 60 degrees and ending at 90 degrees)\n\n"
             "13. Draw an ellipse:\n"
             "    draw_ellipse -> draw_ellipse C (x, y)\n"
             "      example: draw_ellipse C1 (10,15)\n"
             "      (From the cursor C1, draw an ellipse with a minor axis of 10 pixels and a major axis of 15 pixels)\n\n"
             "14. Draw a star:\n"
             "    draw_star -> draw_star C x y\n"
             "      example: draw_star C1 5 10\n"
             "      (From the cursor C1, draw a star with 5 branches, each 10 pixels long)\n\n"
             "15. Fill a shape:\n"
             "    fill_shape -> fill_shape C (R, G, B) (the cursor must be inside the shape)\n"
             "      example: fill_shape C1 (255,0,0)\n"
             "      (From the cursor C1's location, fill the shape with red)\n\n",
        justify="left", wraplength=550)
    commands_label.pack(padx=10, pady=10)

    
    # Advanced instructions section
    advanced_frame = ttk.Frame(notebook)
    notebook.add(advanced_frame, text="Advanced Instructions")
    
    advanced_label = tk.Label(advanced_frame, 
        text="Conditional Instructions:\n\n"
             "1. Example:\n"
             "   if (shape):\n"
             "       draw_square C1 50\n"
             "   else:\n"
             "       draw_circle C1 30\n\n"
             "Loops:\n\n"
             "2. Example:\n"
             "   repeat (5):\n"
             "       move_cursor C1 (10, 10)"
             "Variables:\n\n"
             "3. Example:\n"
             "   var a = 100\n"
             "   draw_circle C1 a\n\n"
             "Functions:\n\n"
             "4. Example:\n"
             "   def my_shape:\n"
             "       draw_square C1 50\n"
             "       draw_circle C1 30\n",
        justify="left", wraplength=550)
    advanced_label.pack(padx=10, pady=10)
    
    # Themes and colors section
    colors_frame = ttk.Frame(notebook)
    notebook.add(colors_frame, text="Themes & Colors")
    
    colors_label = tk.Label(colors_frame, 
        text="Draw++ offers an interactive editor with:\n\n"
             "- Light and dark themes\n"
             "- Highlighting of valid commands and errors\n\n"
             "Colors:\n"
             "- Blue: Simple commands (e.g., create_cursor)\n"
             "- Purple: Conditional instructions (e.g., if, else)\n"
             "- Orange: Loops (e.g., repeat)\n"
             "- Pink: Function (e.g., def)\n"
             "- Green: Geometric shapes (e.g., square, circle)\n"
             "- Red: Syntax errors",
        justify="left", wraplength=550)
    colors_label.pack(padx=10, pady=10)

  # RGB Section
    rgb_frame = ttk.Frame(notebook)
    notebook.add(rgb_frame, text="RGB")

    rgb_label = tk.Label(rgb_frame, 
                          text="Change the color of a cursor using the RGB model:\n\n"
                               "1. Black:\n"
                               "   color_cursor C (0, 0, 0)\n"
                               "      example: color_cursor C1 (0, 0, 0)\n"
                               "      (Fill the selected cursor with black color)\n\n"
                               "2. Blue:\n"
                               "   color_cursor C (0, 0, 255)\n"
                               "      example: color_cursor C1 (0, 0, 255)\n"
                               "      (Fill the selected cursor with blue color)\n\n"
                               "3. Red:\n"
                               "   color_cursor C (255, 0, 0)\n"
                               "      example: color_cursor C1 (255, 0, 0)\n"
                               "      (Fill the selected cursor with red color)\n\n"
                               "4. Green:\n"
                               "   color_cursor C (0, 255, 0)\n"
                               "      example: color_cursor C1 (0, 255, 0)\n"
                               "      (Fill the selected cursor with green color)\n\n"
                               "5. Yellow:\n"
                               "   color_cursor C (255, 255, 0)\n"
                               "      example: color_cursor C1 (255, 255, 0)\n"
                               "      (Fill the selected cursor with yellow color)\n\n",
                          justify="left", wraplength=550)
    rgb_label.pack(padx=10, pady=10)


    # Add a close button
    close_button = ttk.Button(doc_window, text="Close", command=doc_window.destroy)
    close_button.pack(pady=10)
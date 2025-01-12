# A Tkinter-based interactive documentation window for the Draw++ language
import tkinter as tk
from tkinter import ttk

def open_documentation_window():
    """
    Opens an interactive documentation window for Draw++.
    """
    doc_window = tk.Toplevel()
    doc_window.title("Interactive Documentation - Draw++")
    doc_window.geometry("600x500")

    main_frame = ttk.Frame(doc_window)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    content_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

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

    notebook = ttk.Notebook(content_frame)
    notebook.pack(expand=True, fill="both")

    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="General")

    general_label = tk.Label(general_frame, 
        text="Welcome to Draw++!\n\n"
             "Draw++ is a simple language dedicated to geometric drawing.\n"
             "Use specific commands to create shapes, control cursors, and more.\n\n"
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
             "   rotate_cursor -> rotate_cursor C x\n"
             "      example: rotate_cursor C1 90\n"
             "      (Rotate the cursor C1 by 90 degrees)\n\n"
             "6. Change the cursor color:\n"
             "   color_cursor -> color_cursor C (R,G,B)\n"
             "      example: color_cursor C1 (255,0,0)\n"
             "      (Change the color of cursor C1 to red)\n\n"
             "7. Change the cursor thickness:\n"
             "   thickness_cursor -> thickness_cursor C (1, 2, 3, 4, or 5)\n"
             "      example: thickness_cursor C1 4\n"
             "      (Change the thickness of cursor C1 to level 4)\n\n"
             "8. Draw a line:\n"
             "   draw_line -> draw_line C x\n"
             "      example: draw_line C1 20\n"
             "      (From the cursor C1, draw a line of 20 pixels)\n\n",
        justify="left", wraplength=550)
    commands_label.pack(padx=10, pady=10)

    advanced_frame = ttk.Frame(notebook)
    notebook.add(advanced_frame, text="Advanced Instructions")

    advanced_label = tk.Label(advanced_frame, 
        text="Conditional Instructions:\n\n"
             "1. if (condition):\n"
             "instruction_1\n"
             "else:\n"
             "instruction_2\n" 
             " Example:\n"
             "   if (x>15):\n"
             "       draw_square C1 50\n"
             "   else:\n"
             "       draw_circle C1 30\n\n",
        justify="left", wraplength=550)
    advanced_label.pack(padx=10, pady=10)

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

    rgb_frame = ttk.Frame(notebook)
    notebook.add(rgb_frame, text="RGB")

    rgb_label = tk.Label(rgb_frame, 
        text="Change the color of a cursor using the RGB model:\n\n"
             "1. Black:\n"
             "   color_cursor C (0, 0, 0)\n"
             "      example: color_cursor C1 (0, 0, 0)\n\n",
        justify="left", wraplength=550)
    rgb_label.pack(padx=10, pady=10)

    close_button = ttk.Button(doc_window, text="Close", command=doc_window.destroy)
    close_button.pack(pady=10)

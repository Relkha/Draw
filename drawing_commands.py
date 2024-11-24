import tkinter as tk
from cursor_drawing import CursorManager


# Open a drawing window and handle only cursor commands
def open_drawing_window(commands):
    drawing_window = tk.Toplevel()
    drawing_window.title("Cursor Command Window - draw++")
    canvas = tk.Canvas(drawing_window, width=400, height=400, bg="#2e2e2e")  # Dark background
    canvas.pack()
    
    # Initialize the cursor manager with the canvas
    cursor_manager = CursorManager(canvas)

   # Function to apply the selected color to the specified cursor
    def apply_selected_color_to_cursor():
        cursor_name = cursor_name_entry.get()
        r, g, b = int(selected_color[1:3], 16), int(selected_color[3:5], 16), int(selected_color[5:7], 16)
        color_command = f"color_cursor {cursor_name} to {r} {g} {b}"
        cursor_manager.execute_command(color_command)

    # Execute initial commands
    for command in commands:
        cursor_manager.execute_command(command)


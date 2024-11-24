import tkinter as tk

class ColorSelector:
    def __init__(self, parent, apply_color_callback):
        self.apply_color_callback = apply_color_callback  # Function to apply the color

        # Create a Toplevel window for color selection
        self.color_window = tk.Toplevel(parent)
        self.color_window.title("RGB Color Selector")
        self.color_window.geometry("300x150")
        self.color_window.configure(bg="#1e1e1e")

        # Initialize color values
        self.red, self.green, self.blue = 0, 0, 0

        # Red slider
        tk.Label(self.color_window, text="Red", bg="#1e1e1e", fg="white").grid(row=0, column=0)
        self.red_scale = tk.Scale(self.color_window, from_=0, to=255, orient="horizontal", bg="#333333", fg="white", command=self.update_red)
        self.red_scale.grid(row=1, column=0, padx=5)

        # Green slider
        tk.Label(self.color_window, text="Green", bg="#1e1e1e", fg="white").grid(row=0, column=1)
        self.green_scale = tk.Scale(self.color_window, from_=0, to=255, orient="horizontal", bg="#333333", fg="white", command=self.update_green)
        self.green_scale.grid(row=1, column=1, padx=5)

        # Blue slider
        tk.Label(self.color_window, text="Blue", bg="#1e1e1e", fg="white").grid(row=0, column=2)
        self.blue_scale = tk.Scale(self.color_window, from_=0, to=255, orient="horizontal", bg="#333333", fg="white", command=self.update_blue)
        self.blue_scale.grid(row=1, column=2, padx=5)

        # Apply button
        self.apply_button = tk.Button(self.color_window, text="Apply Color", command=self.apply_color, bg="#444444", fg="white")
        self.apply_button.grid(row=2, column=1, pady=10)

    # Update functions for RGB values
    def update_red(self, value):
        self.red = int(value)

    def update_green(self, value):
        self.green = int(value)

    def update_blue(self, value):
        self.blue = int(value)

    # Function to return the selected color in hex format
    def apply_color(self):
        selected_color = f'#{self.red:02x}{self.green:02x}{self.blue:02x}'
        self.apply_color_callback(selected_color)  # Call the provided callback with the selected color
        self.color_window.destroy()  # Close the color selector window


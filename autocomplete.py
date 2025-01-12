# This script integrates an autocomplete feature for a text widget, leveraging keywords from a JSON file.
# It dynamically suggests completions based on the user's input and processes the content for syntax highlighting.

import tkinter as tk
import json
from analyse_input import process_and_color_line_by_line_with_blocks

# Load keywords from commandes.json
def load_keywords():
    with open("commandes.json", "r") as file:
        data = json.load(file)
    keywords = list(data["commands"].keys()) + list(data["function"].keys()) + list(data["conditionals"].keys()) + list(data["loops"].keys())
    return keywords

# Autocomplete functionality
class Autocomplete:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.suggestion_box = None
        self.keywords = load_keywords()
        self.suppress_analysis = False  # Flag to temporarily suppress analysis
        self.current_suggestion = None  # Track the current inserted suggestion

        # Bind the text widget for autocomplete
        self.text_widget.bind("<KeyRelease>", self.on_key_release)

    def enable(self):
        """
        Enables analysis after initialization.
        """
        self.suppress_analysis = False

    def disable(self):
        """
        Temporarily disables analysis.
        """
        self.suppress_analysis = True
        
    def on_key_release(self, event):
        if self.suppress_analysis:
            return  # Block any analysis temporarily

        self.close_suggestions()
        self.current_suggestion = None

        # Autocomplete logic...
        current_line = self.text_widget.get("insert linestart", "insert")
        last_word = current_line.split()[-1] if current_line.split() else ""

        # Find possible suggestions
        suggestions = [kw for kw in self.keywords if kw.startswith(last_word)]

        if suggestions and last_word:
            self.show_suggestions(suggestions)

        # Re-trigger analysis after regular input
        process_and_color_line_by_line_with_blocks(self.text_widget)

    def show_suggestions(self, suggestions):
        """
        Displays a list of suggestions near the cursor.
        """
        if self.suggestion_box:
            self.suggestion_box.destroy()

        # Position the suggestion box
        x, y, _, _ = self.text_widget.bbox("insert")
        x_offset, y_offset = x + 20, y + 25

        self.suggestion_box = tk.Toplevel()
        self.suggestion_box.wm_overrideredirect(True)
        self.suggestion_box.geometry(f"+{self.text_widget.winfo_rootx() + x_offset}+{self.text_widget.winfo_rooty() + y_offset}")

        listbox = tk.Listbox(self.suggestion_box, bg="white", fg="black", selectbackground="gray", highlightthickness=0)
        for suggestion in suggestions:
            listbox.insert(tk.END, suggestion)
        listbox.pack()

        listbox.bind("<<ListboxSelect>>", lambda e: self.insert_suggestion(listbox))

    def insert_suggestion(self, listbox):
        self.suppress_analysis = True  # Disable analysis during insertion
        selected = listbox.get(listbox.curselection())
        self.current_suggestion = selected

        # Add a separator point for Undo/Redo
        self.text_widget.edit_separator()

        # Delete the current word and insert the suggestion
        self.text_widget.delete("insert-1c wordstart", "insert")
        self.text_widget.insert("insert", selected + " ")

        # Add another separator point for Undo/Redo after insertion
        self.text_widget.edit_separator()

        self.close_suggestions()
        self.suppress_analysis = False  # Re-enable analysis
        process_and_color_line_by_line_with_blocks(self.text_widget)

    def close_suggestions(self):
        if self.suggestion_box:
            self.suggestion_box.destroy()
            self.suggestion_box = None

import tkinter as tk
from tkinter import filedialog, Text, ttk
from drawing_commands import open_drawing_window
from color_selector import ColorSelector

# Dictionnaire pour stocker les fonctions associées aux commandes de menus
menu_commands = {}

# Liste pour stocker les chemins des fichiers ouverts
file_paths = []

# Fonction pour ouvrir un fichier avec l'extension .draw
def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".draw", filetypes=[("draw++ files", "*.draw"), ("All files", "*.*")])
    if file_path:
        file_paths.append(file_path)
        text_area.delete(1.0, tk.END)
        with open(file_path, 'r') as file:
            text_area.insert(1.0, file.read())

# Fonction pour enregistrer un fichier avec l'extension .draw
def save_file():
    if not file_paths:
        file_path = filedialog.asksaveasfilename(defaultextension=".draw", filetypes=[("draw++ files", "*.draw"), ("All files", "*.*")])
        if file_path:
            file_paths.append(file_path)
    else:
        file_path = file_paths[-1]

    with open(file_path, 'w') as file:
        file.write(text_area.get(1.0, tk.END))

# Fonction pour créer un nouveau fichier
def new_file():
    text_area.delete(1.0, tk.END)
    file_paths.clear()

# Dictionnaire des commandes du menu fichier
menu_commands['Fichier'] = {
    'Nouveau': new_file,
    'Ouvrir': open_file,
    'Enregistrer': save_file,
    'Quitter': lambda: root.quit()
}

# Fonction pour annuler l'action
def undo_action():
    text_area.edit_undo()

# Fonction pour répéter l'action annulée
def redo_action():
    text_area.edit_redo()

# Dictionnaire des commandes du menu édition
menu_commands['Édition'] = {
    'Annuler': undo_action,
    'Répéter': redo_action
}

# Créer la fenêtre principale
root = tk.Tk()
root.title("Text Edition - draw++")
root.geometry("700x500")
root.configure(bg="#1e1e1e")  # Dark background color

# Zone de texte with dark mode styling
text_area = Text(
    root, wrap='word', undo=True,
    font=("Helvetica", 12), bg="#2e2e2e", fg="#ffffff", insertbackground="white",
    relief="flat", padx=10, pady=10
)
text_area.pack(expand=True, fill='both', padx=10, pady=10)

# Menu styling
menu_bar = tk.Menu(root, background="#333333", foreground="white", activebackground="#555555", activeforeground="white")
root.config(menu=menu_bar)

# Function to create menus dynamically (unchanged).
def create_menus(menu_dict):
    for menu_name, commands in menu_dict.items():
        menu = tk.Menu(menu_bar, tearoff=0, background="#333333", foreground="white", activebackground="#555555", activeforeground="white")
        menu_bar.add_cascade(label=menu_name, menu=menu)
        for command_name, command_func in commands.items():
            menu.add_command(label=command_name, command=command_func)

create_menus(menu_commands)

# Define run_draw_commands function before using it in the button
def run_draw_commands():
    # Get text from the editing area and split into command lines
    commands = text_area.get("1.0", tk.END).strip().splitlines()
    open_drawing_window(commands)  # Send commands for cursor-only execution

# Button styling for dark mode
style = ttk.Style()
style.theme_use("default")
style.configure(
    "TButton",
    font=("Helvetica", 10), padding=6,
    background="#444444", foreground="white"
)
style.map("TButton", background=[("active", "#666666")])

# Placeholder for color to be set by ColorSelector
selected_color = "#000000"

# Function to handle color application from ColorSelector
def set_selected_color(color):
    global selected_color
    selected_color = color

# Function to open the ColorSelector and set color
def open_color_selector():
    ColorSelector(root, set_selected_color)

# Button to execute commands
run_button = ttk.Button(root, text="Exécuter les commandes de curseur", command=run_draw_commands, style="TButton")
run_button.place(relx=1, y=5, anchor="ne")

# Button to open the color selector
color_button = tk.Button(root, text="Choose Color", command=open_color_selector, bg="#444444", fg="white")
color_button.pack(pady=5)


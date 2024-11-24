import tkinter as tk
from text_edition import root, text_area, menu_commands, create_menus  # Importer les composants depuis text_edition.py
from drawing_commands import open_drawing_window


def run_draw_commands():
    # Obtenir le texte de la zone d'édition et le diviser en lignes de commandes
    commands = text_area.get("1.0", tk.END).splitlines()
    open_drawing_window(commands)  # Ouvrir la fenêtre de dessin et interpréter les commandes


root.mainloop()

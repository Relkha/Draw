import tkinter as tk
from tkinter import ttk

def open_documentation_window():
    """
    Fonction pour ouvrir une fenêtre de documentation interactive.
    """
    # Créer une nouvelle fenêtre
    doc_window = tk.Toplevel()
    doc_window.title("Documentation Interactive - Draw++")
    doc_window.geometry("600x500")
    
    # Créer un widget Notebook pour organiser les sections
    notebook = ttk.Notebook(doc_window)
    notebook.pack(expand=True, fill="both")
    
    # Section générale
    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="Général")
    
    general_label = tk.Label(general_frame, 
        text="Bienvenue dans Draw++ !\n\n"
             "Draw++ est un langage simple dédié au dessin géométrique.\n"
             "Utilisez des commandes spécifiques pour créer des formes, "
             "contrôler les curseurs, et bien plus encore.\n\n"
             "Les catégories d'instructions sont :\n"
             "- Commandes simples\n"
             "- Instructions conditionnelles (if...else)\n"
             "- Boucles (repeat)",
        justify="left", wraplength=550)
    general_label.pack(padx=10, pady=10)
    
    # Section commandes simples
    commands_frame = ttk.Frame(notebook)
    notebook.add(commands_frame, text="Commandes Simples")
    
    commands_label = tk.Label(commands_frame, 
        text="Exemples de commandes simples :\n\n"
             "1. Créer un curseur :\n"
             "   create_cursor C1 (150, 100)\n\n"
             "2. Déplacer un curseur :\n"
             "   move_cursor C1 (200, 300)\n\n"
             "3. Dessiner un carré :\n"
             "   draw_square C1 50\n\n"
             "4. Dessiner un cercle :\n"
             "   draw_circle C1 30",
        justify="left", wraplength=550)
    commands_label.pack(padx=10, pady=10)
    
    # Section instructions évoluées
    advanced_frame = ttk.Frame(notebook)
    notebook.add(advanced_frame, text="Instructions Évoluées")
    
    advanced_label = tk.Label(advanced_frame, 
        text="Instructions Conditionnelles :\n\n"
             "1. Exemple :\n"
             "   if (shape):\n"
             "       draw_square C1 50\n"
             "   else:\n"
             "       draw_circle C1 30\n\n"
             "Boucles :\n\n"
             "2. Exemple :\n"
             "   repeat (5):\n"
             "       move_cursor C1 (10, 10)",
        justify="left", wraplength=550)
    advanced_label.pack(padx=10, pady=10)
    
    # Section couleurs et thèmes
    colors_frame = ttk.Frame(notebook)
    notebook.add(colors_frame, text="Thèmes & Couleurs")
    
    colors_label = tk.Label(colors_frame, 
        text="Draw++ propose un éditeur interactif avec :\n\n"
             "- Thème clair et sombre\n"
             "- Mise en surbrillance des commandes valides et erreurs\n\n"
             "Couleurs :\n"
             "- Bleu : Commandes simples (ex: create_cursor)\n"
             "- Violet : Instructions conditionnelles (ex: if, else)\n"
             "- Orange : Boucles (ex: repeat)\n"
             "- Vert : Formes géométriques (ex: square, circle)\n"
             "- Rouge : Erreurs de syntaxe",
        justify="left", wraplength=550)
    colors_label.pack(padx=10, pady=10)
    
    # Ajouter un bouton de fermeture
    close_button = ttk.Button(doc_window, text="Fermer", command=doc_window.destroy)
    close_button.pack(pady=10)

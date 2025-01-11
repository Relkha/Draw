import tkinter as tk
from tkinter import filedialog, simpledialog, Text, ttk
from analyse_input import process_and_color_line_by_line_with_blocks
from lexer import Lexer
from parser import Parser
from generate_comile_exect_c import generate_and_compile
from autocomplete import Autocomplete
from interactive_doc import open_documentation_window



# Créer la fenêtre principale
root = tk.Tk()
root.title("Text Edition - Draw++")
root.geometry("700x500")

# Créer un conteneur d'onglets (Notebook)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Liste pour stocker les fichiers ouverts
open_files = {}

# Initialiser le mode sombre par défaut
is_dark_mode = False  # Par défaut, mode lumineux


# Fonction pour appliquer le thème à un widget spécifique
def apply_theme_to_widget(text_widget):
    if is_dark_mode:  # Thème sombre
        text_widget.configure(bg="#1e1e1e", fg="white", insertbackground="white")
    else:  # Thème clair
        text_widget.configure(bg="white", fg="black", insertbackground="black")

    configure_tags(text_widget)  # Reconfigurer les tags

def apply_default_tag(text_widget):
    text_widget.tag_add("default", "1.0", "end")  # Appliquer le tag "default" à tout le texte

# Fonction pour configurer les tags de mise en forme
def configure_tags(text_widget):
    if is_dark_mode:  # Configuration en mode sombre
        text_widget.tag_configure("keyword", foreground="cyan", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("conditional", foreground="violet", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("loop", foreground="orange", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("shape", foreground="green", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("function", foreground="pink", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("valid", foreground="white")  # Texte valide en blanc
        text_widget.tag_configure("incorrect", foreground="red")  # Erreur en rouge
        text_widget.tag_configure("default", foreground="white")  # Par défaut en blanc
    else:  # Configuration en mode clair
        text_widget.tag_configure("keyword", foreground="blue", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("conditional", foreground="purple", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("loop", foreground="orange", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("shape", foreground="green", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("function", foreground="pink", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("valid", foreground="black")  # Texte valide en noir
        text_widget.tag_configure("incorrect", foreground="red")  # Erreur en rouge
        text_widget.tag_configure("default", foreground="black")  # Par défaut en noir



#Fonction pour les frappes par onglets
def on_key_release(event, text_widget):
    if text_widget in open_files:
        undo_stack = open_files[text_widget]["undo_stack"]
        current_content = text_widget.get("1.0", "end-1c")  # Récupérer le contenu actuel

        # Ajouter le contenu actuel à l'historique
        if not undo_stack or undo_stack[-1] != current_content:  # Éviter les doublons
            undo_stack.append(current_content)
    process_and_color_line_by_line_with_blocks(text_widget)  # Analyse et met en surbrillance

# Fonction pour créer un nouvel onglet avec une zone de texte
def create_new_tab(title="New File"):
    text_widget = Text(notebook, wrap='word', undo=True, font=("Helvetica", 12), relief="flat", padx=10, pady=10)
    configure_tags(text_widget)
    
    text_widget.bind("<KeyRelease>", lambda event: on_key_release(event, text_widget))
    # Ajouter l'onglet au notebook
    notebook.add(text_widget, text=title)
    notebook.select(text_widget)
    
    open_files[text_widget] = {
        "path": None,
        "undo_stack": [],  # Historique des actions annulées
        "redo_stack": []   # Historique des actions répétées
    }
    # Appliquer le thème dès la création de l'onglet
    apply_theme_to_widget(text_widget)
    autocomplete = Autocomplete(text_widget)
    return text_widget

# Fonction pour fermer un onglet
def close_tab(tab_title):
    if tab_title in open_files:
        # Supprimer l'onglet du notebook et du dictionnaire open_files
        current_tab = notebook.index(tab_title)
        notebook.forget(current_tab)
        del open_files[tab_title]

# Fonction pour renommer l'onglet actif
def rename_tab():
    # Obtenir l'index et le titre actuel de l'onglet actif
    current_tab_index = notebook.index("current")
    current_title = notebook.tab(current_tab_index, "text")
    # Demander un nouveau titre
    new_title = simpledialog.askstring("Rename tab", "Enter a new name:", initialvalue=current_title)
    if not new_title or new_title.strip() == current_title:  # Si annulé ou identique
        return
    new_title = new_title.strip()
    # Vérifier que le titre actuel existe dans `open_files`
    if current_title not in open_files:
        open_files[current_title] = {"path": None, "text_widget": None}  # Ajouter si manquant
    # Vérifier que le nouveau titre n'existe pas déjà
    if new_title in open_files:
        tk.messagebox.showerror("Error", f"The tab '{new_title}' already exist.")
        return
    # Mettre à jour dans `open_files` et `notebook`
    open_files[new_title] = open_files.pop(current_title)  # Renommer dans le dictionnaire
    notebook.tab(current_tab_index, text=new_title)  # Renommer dans le notebook

# Fonction pour ouvrir un fichier
def open_file():
   file_path = filedialog.askopenfilename(defaultextension=".draw", filetypes=[("Draw files", "*.draw"), ("All files", "*.*")])
   if file_path:
        # Vérifier si le fichier est déjà ouvert
        for text_widget, data in open_files.items():
            if data.get("path") == file_path:
                tk.messagebox.showinfo("Info", f"The file '{file_path}' is already open.")
                return  # Ne pas ouvrir le fichier une deuxième fois
        # Si le fichier n'est pas encore ouvert
        file_name = file_path.split('/')[-1]  # Obtenir le nom du fichier
        with open(file_path, 'r') as file:
            content = file.read()
        # Créer un nouvel onglet pour ce fichier
        text_widget = create_new_tab(file_name)
        text_widget.insert("1.0", content)  # Charger le contenu dans le widget
        text_widget.edit_modified(False)  # Réinitialiser l'état modifié
        # Ajouter le fichier à `open_files`
        open_files[text_widget] = {
            "path": file_path,
            "undo_stack": [],
            "redo_stack": []
        }

# Fonction pour sauvegarder un fichier
def save_file():
    current_tab_widget = notebook.nametowidget(notebook.select())  # Obtenir le widget actif
    if current_tab_widget in open_files:  # Vérifier que le widget est suivi
        text_widget = current_tab_widget
        content = text_widget.get("1.0", "end-1c")  # Récupérer le contenu du widget
        file_path = filedialog.asksaveasfilename(defaultextension=".draw", filetypes=[("Draw files", "*.draw"), ("All files", "*.*")])
        if file_path:
            # Sauvegarder le fichier
            with open(file_path, 'w') as file:
                file.write(content)
            
            # Mettre à jour le chemin du fichier dans `open_files`
            open_files[text_widget]['path'] = file_path
            
            # Extraire le nom du fichier pour l'utiliser comme titre
            file_name = file_path.split('/')[-1]
            notebook.tab(current_tab_widget, text=file_name)  # Mettre à jour le titre de l'onglet
    else:
        tk.messagebox.showerror("Error", "No active file found to save.")

# Fonction pour fermer l'onglet actif
def close_active_tab():
    current_tab_index = notebook.index("current")  # Récupérer l'index de l'onglet actif
    if current_tab_index >= 0:
        current_title = notebook.tab(current_tab_index, "text")  # Obtenir le titre de l'onglet
        # Supprimer l'onglet du notebook et du dictionnaire open_files
        notebook.forget(current_tab_index)
        if current_title in open_files:
            del open_files[current_title]

# Fonction pour annuler l'action
def undo_action():
    try:
        # Obtenir le widget actif
        current_tab_widget = notebook.nametowidget(notebook.select())  # Widget actif

        if current_tab_widget in open_files:
            text_widget = current_tab_widget
            undo_stack = open_files[text_widget]["undo_stack"]
            redo_stack = open_files[text_widget]["redo_stack"]

            # Si l'historique contient des actions à annuler
            if undo_stack:
                last_action = undo_stack.pop()  # Récupérer la dernière action
                redo_stack.append(last_action)  # Ajouter à l'historique "redo"
                text_widget.delete("1.0", "end")  # Effacer le texte actuel
                text_widget.insert("1.0", last_action)  # Restaurer l'état précédent

                # Analyse et mise en surbrillance après modification
                process_and_color_line_by_line_with_blocks(text_widget)
            else:
                tk.messagebox.showinfo("Info", "No action to undo.")
        else:
            tk.messagebox.showerror("Error", "No active widget found in `open_files`.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error during undo: {e}")

# Fonction pour répéter l'action annulée
def redo_action():
    try:
        # Obtenir le widget actif
        current_tab_widget = notebook.nametowidget(notebook.select())  # Widget actif

        if current_tab_widget in open_files:
            text_widget = current_tab_widget
            undo_stack = open_files[text_widget]["undo_stack"]
            redo_stack = open_files[text_widget]["redo_stack"]

            # Si des actions peuvent être répétées
            if redo_stack:
                last_redo = redo_stack.pop()  # Récupérer l'action à refaire
                undo_stack.append(last_redo)  # Ajouter à l'historique "undo"
                text_widget.delete("1.0", "end")  # Effacer le texte actuel
                text_widget.insert("1.0", last_redo)  # Restaurer l'état précédent

                # Analyse et mise en surbrillance après modification
                process_and_color_line_by_line_with_blocks(text_widget)
            else:
                tk.messagebox.showinfo("Info", "No action to redo.")
        else:
            tk.messagebox.showerror("Error", "No active widget found in `open_files`. `open_files`.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error during redo: {e}")

# Fonction pour basculer entre mode sombre et lumineux
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode  # Basculer entre mode clair et mode sombre
    
    # Obtenir le widget de texte actif
    current_tab_widget = notebook.nametowidget(notebook.select())  # Widget actif
    if current_tab_widget in open_files:  # Vérifier que le widget est suivi
        apply_theme_to_widget(current_tab_widget)  # Appliquer le thème au widget actif
    else:
        tk.messagebox.showerror("Error", "Unable to find the active tab.")

def analyze_and_extract_commands(user_input):
    lines = user_input.splitlines() if isinstance(user_input, str) else user_input
    commands_data = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:  # Ignorer les lignes vides
            i += 1
            continue

        if "{" in line:  # Début d'un bloc
            block_content = []
            iteration_count = 0
            function_name = ""

            if line.startswith("repeat"):
                iteration_count = int(line.split("(")[1].split(")")[0])
            elif line.startswith("def"):
                function_name = line.split()[1]

            # Collecte du contenu du bloc
            while i < len(lines):
                block_line = lines[i].strip()
                if "}" in block_line:  # Fin du bloc
                    block_content.append(block_line.split("}")[0].strip())
                    break
                elif "{" not in block_line:
                    block_content.append(block_line)
                i += 1

            # Analyser les sous-commandes du bloc
            block_content_parsed = []
            for block_line in block_content:
                if not block_line:  # Ignorer les lignes vides
                    continue
                lexer = Lexer(block_line)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                is_valid, error_message = parser.parse()

                if is_valid:
                    block_command_data = extract_command_data(tokens)
                    block_content_parsed.append(block_command_data)
                else:
                    print(f"Erreur de syntaxe dans le bloc : {error_message}")

            if iteration_count:
                commands_data.append({
                    'command': 'repeat',
                    'iterations': iteration_count,
                    'block': block_content_parsed
                })
            elif function_name:
                commands_data.append({
                    'command': 'def',
                    'name': function_name,
                    'block': block_content_parsed
                })
        else:
            # Commandes simples
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            is_valid, error_message = parser.parse()

            if is_valid:
                command_data = extract_command_data(tokens)
                commands_data.append(command_data)
            else:
                print(f"Erreur de syntaxe : {error_message}")

        i += 1

    return commands_data


def extract_command_data(tokens):
    """
    Transforme les tokens en un dictionnaire de commande valide.
    :param tokens: Liste des tokens générés par le Lexer.
    :return: Un dictionnaire représentant la commande extraite.
    """
    command_data = {}

    if tokens[0][1] == 'create_cursor' and len(tokens) == 7:
        command_data = {
            'command': 'create_cursor',
            'name': tokens[1][1],
            'x': int(tokens[3][1]),
            'y': int(tokens[5][1])
        }
    elif tokens[0][1] == 'move_cursor' and len(tokens) == 7:
        command_data = {
            'command': 'move_cursor',
            'name': tokens[1][1],
            'x': int(tokens[3][1]),
            'y': int(tokens[5][1])
        }
    elif tokens[0][1] == 'color_cursor' and len(tokens) == 9:
        command_data = {
            'command': 'color_cursor',
            'name': tokens[1][1],
            'r': int(tokens[3][1]),
            'g': int(tokens[5][1]),
            'b': int(tokens[7][1])
        }
    elif tokens[0][1] == 'draw_line' and len(tokens) == 3:
        command_data = {
            'command': 'draw_line',
            'name': tokens[1][1],
            'length': int(tokens[2][1])
        }
    elif tokens[0][1] == 'show_cursor' and len(tokens) == 2:
        command_data = {
            'command': 'show_cursor',
            'name': tokens[1][1]
        }
    elif tokens[0][1] == 'hide_cursor' and len(tokens) == 2:
        command_data = {
            'command': 'hide_cursor',
            'name': tokens[1][1]
        }
    elif tokens[0][1] == 'rotate_cursor' and len(tokens) == 3:
        command_data = {
            'command': 'rotate_cursor',
            'name': tokens[1][1],
            'angle': int(tokens[2][1])
        }
    elif tokens[0][1] == 'thickness_cursor' and len(tokens) == 3:
        command_data = {
            'command': 'thickness_cursor',
            'name': tokens[1][1],
            'thickness': int(tokens[2][1])
        }
    elif tokens[0][1] == 'draw_rectangle' and len(tokens) == 7:
        command_data = {
            'command': 'draw_rectangle',
            'name': tokens[1][1],
            'width': int(tokens[3][1]),
            'height': int(tokens[5][1])
        }
    elif tokens[0][1] == 'draw_square' and len(tokens) == 3:
        command_data = {
            'command': 'draw_square',
            'name': tokens[1][1],
            'size': int(tokens[2][1])
        }
    elif tokens[0][1] == 'draw_circle' and len(tokens) == 3:
        command_data = {
            'command': 'draw_circle',
            'name': tokens[1][1],
            'radius': int(tokens[2][1])
        }
    elif tokens[0][1] == 'draw_arc' and len(tokens) == 5:
        command_data = {
            'command': 'draw_arc',
            'name': tokens[1][1],
            'radius': int(tokens[2][1]),
            'start_angle': int(tokens[3][1]),
            'end_angle': int(tokens[4][1])
        }
    elif tokens[0][1] == 'draw_ellipse' and len(tokens) == 7:
        command_data = {
            'command': 'draw_ellipse',
            'name': tokens[1][1],
            'width': int(tokens[3][1]),
            'height': int(tokens[5][1])
        }
    elif tokens[0][1] == 'draw_star' and len(tokens) == 4:
        command_data = {
            'command': 'draw_star',
            'name': tokens[1][1],
            'branches': int(tokens[2][1]),
            'size': int(tokens[3][1])
        }
    elif tokens[0][1] == 'fill_shape' and len(tokens) == 9:
        command_data = {
            'command': 'fill_shape',
            'name': tokens[1][1],
            'r': int(tokens[3][1]),
            'g': int(tokens[5][1]),
            'b': int(tokens[7][1])
        }
    else:
        print(f"Erreur : commande non reconnue ou syntaxe incorrecte pour les tokens : {tokens}")

    return command_data


# Fonction pour exécuter les commandes de dessin
def run_draw_commands():
    try:
        current_tab_widget = notebook.nametowidget(notebook.select())  # Onglet actuellement sélectionné
        if current_tab_widget in open_files:
            commands = current_tab_widget.get("1.0", tk.END).strip().splitlines()
            c = analyze_and_extract_commands(commands)
            generate_and_compile (c)
        else:
            tk.messagebox.showerror("Error", "Unable to find the active tab to execute the commands.")
    except Exception as e:
        tk.messagebox.showerror("Error",f"Error during execution: {e}")

# Dictionnaire des commandes de menu
menu_commands = {
    'File': {
        'New Tab': lambda: create_new_tab(),
        'Open File': open_file,
        'Save File': save_file,
        'Close Tab': close_active_tab,
        'Rename Tab': rename_tab,
        'Quit': lambda: root.destroy()
    },
    'Edit': {
        'Undo': undo_action,
        'Redo': redo_action
    },
    'Brightness': {
        'Toggle mode': toggle_theme
    },
    'Help': {
        'Documentation': open_documentation_window  # Lancer la documentation interactive
    }
}

# Création du menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
for menu_name, commands in menu_commands.items():
    menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=menu_name, menu=menu)
    for command_name, command_func in commands.items():
        menu.add_command(label=command_name, command=command_func)

# Ajouter un bouton pour exécuter les commandes et le positionner en haut à droite
def position_run_button():
    run_button.place(x=root.winfo_width() - 200, y=10)  # Positionner le bouton en haut à droite

run_button = ttk.Button(root, text="Execute commands", command=run_draw_commands)
root.after(100, position_run_button)  # S'assurer que la fenêtre est prête avant de positionner le bouton

# Créer un premier onglet
create_new_tab()

# Appliquer le thème à tous les onglets existants au démarrage
for file_data in open_files.values():
    if 'text_widget' in file_data and file_data['text_widget'] is not None:
        apply_theme_to_widget(file_data['text_widget'])

# Lancer l'application
root.mainloop()

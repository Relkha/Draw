import tkinter as tk
from tkinter import filedialog, simpledialog, Text, ttk
from analyse_input import analyze_and_highlight
from lexer import Lexer
from parser import Parser
from generate_comile_exect_c import generate_and_compile
from autocomplete import Autocomplete
from interactive_doc import open_documentation_window



# Créer la fenêtre principale
root = tk.Tk()
root.title("Text Edition - draw++")
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
        text_widget.tag_configure("function", foreground="cyan", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("conditional", foreground="violet", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("loop", foreground="orange", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("shape", foreground="green", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("valid", foreground="white")  # Texte valide en blanc
        text_widget.tag_configure("incorrect", foreground="red")  # Erreur en rouge
        text_widget.tag_configure("default", foreground="white")  # Par défaut en blanc
    else:  # Configuration en mode clair
        text_widget.tag_configure("function", foreground="blue", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("conditional", foreground="purple", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("loop", foreground="orange", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("shape", foreground="green", font=("Helvetica", 10, "bold"))
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
    analyze_and_highlight(text_widget)  # Analyse et met en surbrillance

# Fonction pour créer un nouvel onglet avec une zone de texte
def create_new_tab(title="Nouveau fichier"):
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
    new_title = simpledialog.askstring("Renommer l'onglet", "Entrez un nouveau nom :", initialvalue=current_title)
    if not new_title or new_title.strip() == current_title:  # Si annulé ou identique
        return
    new_title = new_title.strip()
    # Vérifier que le titre actuel existe dans `open_files`
    if current_title not in open_files:
        open_files[current_title] = {"path": None, "text_widget": None}  # Ajouter si manquant
    # Vérifier que le nouveau titre n'existe pas déjà
    if new_title in open_files:
        tk.messagebox.showerror("Erreur", f"L'onglet '{new_title}' existe déjà.")
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
                tk.messagebox.showinfo("Info", f"Le fichier '{file_path}' est déjà ouvert.")
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
        tk.messagebox.showerror("Erreur", "Aucun fichier actif trouvé à enregistrer.")

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
                analyze_and_highlight(text_widget)
            else:
                tk.messagebox.showinfo("Info", "Aucune action à annuler.")
        else:
            tk.messagebox.showerror("Erreur", "Aucun widget actif trouvé dans `open_files`.")
    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Erreur lors de l'annulation : {e}")

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
                analyze_and_highlight(text_widget)
            else:
                tk.messagebox.showinfo("Info", "Aucune action à répéter.")
        else:
            tk.messagebox.showerror("Erreur", "Aucun widget actif trouvé dans `open_files`.")
    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Erreur lors de la répétition : {e}")

# Fonction pour basculer entre mode sombre et lumineux
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode  # Basculer entre mode clair et mode sombre
    
    # Obtenir le widget de texte actif
    current_tab_widget = notebook.nametowidget(notebook.select())  # Widget actif
    if current_tab_widget in open_files:  # Vérifier que le widget est suivi
        apply_theme_to_widget(current_tab_widget)  # Appliquer le thème au widget actif
    else:
        tk.messagebox.showerror("Erreur", "Impossible de trouver l'onglet actif.")

def analyze_and_extract_commands(user_input):
    # Si l'entrée est une liste (comme pour plusieurs lignes de texte), on la garde telle quelle.
    if isinstance(user_input, list):
        lines = user_input
    else:
        # Si c'est une chaîne, on la découpe en lignes.
        lines = user_input.splitlines()

    # Liste pour stocker toutes les données extraites des commandes
    commands_data = []

    # Analyser chaque ligne de commande
    for line in lines:
        print(f"\nAnalyzing line: {line}")  # Print the current line being analyzed

        # Créer un lexer pour analyser chaque ligne
        lexer = Lexer(line)
        tokens = lexer.tokenize()  # Obtenir les tokens de la ligne

        print(f"Tokens: {tokens}")  # Print the tokens generated by the lexer

        # Utiliser le parser pour valider la ligne
        parser = Parser(tokens)
        is_valid, error_token = parser.parse()

        print(f"Is valid: {is_valid}, Error: {error_token}")  # Print the validation result

        if is_valid:
            # Si la commande est valide, extraire les données
            command_data = {}

            # Affichage détaillé des tokens avant l'extraction
            print(f"First token: {tokens[0]}")  # Affichage du premier token
            print(f"Second token: {tokens[1]}")  # Affichage du deuxième token

            if tokens[0][1] == 'create_cursor' and len(tokens) == 7:
                # Commande create_cursor : Nom, X, Y (ignorer les parenthèses et la virgule)
                command_data = {
                    'command': 'create_cursor',
                    'name': tokens[1][1],  # Le nom du curseur
                    'x': int(tokens[3][1]),  # Coordonnée X (après '(')
                    'y': int(tokens[5][1])   # Coordonnée Y (avant ')')
                }
                print(f"Extracted create_cursor data: {command_data}")  # Affichage des données extraites
            elif tokens[0][1] == 'move_cursor' and len(tokens) == 7:
                # Commande move_cursor : Nom, X, Y
                command_data = {
                    'command': 'move_cursor',
                    'name': tokens[1][1],  # Le nom du curseur
                    'x': int(tokens[3][1]),  # Coordonnée X
                    'y': int(tokens[5][1])   # Coordonnée Y
                }
                print(f"Extracted move_cursor data: {command_data}")  # Affichage des données extraites
            elif tokens[0][1] == 'color_cursor' and len(tokens) == 9:
                # Commande color_cursor : Nom, R, G, B
                command_data = {
                    'command': 'color_cursor',
                    'name': tokens[1][1],  # Le nom du curseur
                    'r': int(tokens[3][1]),  # Couleur R
                    'g': int(tokens[5][1]),  # Couleur G
                    'b': int(tokens[7][1])   # Couleur B
                }
                print(f"Extracted color_cursor data: {command_data}")  # Affichage des données extraites
            elif tokens[0][1] == 'draw_line' and len(tokens) == 3:
                # Commande draw_line : Nom, longueur
                command_data = {
                    'command': 'draw_line',
                    'name': tokens[1][1],  # Le nom du curseur
                    'length': int(tokens[2][1])  # Longueur de la ligne
                }
                print(f"Extracted draw_line data: {command_data}")
            elif tokens[0][1] == 'show_cursor' and len(tokens) == 2:
                # Commande show_cursor : Nom
                command_data = {
                    'command': 'show_cursor',
                    'name': tokens[1][1]  # Le nom du curseur
                }
                print(f"Extracted show_cursor data: {command_data}")

            elif tokens[0][1] == 'hide_cursor' and len(tokens) == 2:
                # Commande hide_cursor : Nom
                command_data = {
                    'command': 'hide_cursor',
                    'name': tokens[1][1]  #Le nom du curseur
                }
                print(f"Extracted hide_cursor data: {command_data}")

            elif tokens[0][1] == 'rotate_cursor' and len(tokens) == 3:
                 # Commande rotate_cursor : Nom, angle
                command_data = {
                    'command': 'rotate_cursor',
                    'name': tokens[1][1],  # Le nom du curseur
                    'angle': int(tokens[2][1])  # Angle en degrés
                }
                print(f"Extracted rotate_cursor data: {command_data}")

            elif tokens[0][1] == 'thickness_cursor' and len(tokens) == 3:
                # Commande thickness_cursor : Nom, épaisseur
                command_data = {
                    'command': 'thickness_cursor',
                    'name': tokens[1][1],  # Le nom du curseur
                    'thickness': int(tokens[2][1])  # Épaisseur
                }
                print(f"Extracted thickness_cursor data: {command_data}")

            elif tokens[0][1] == 'draw_rectangle' and len(tokens) == 7:
                # Commande draw_rectangle : Nom, dimensions (x, y)
                print("Debug.")
                command_data = {
                    'command': 'draw_rectangle',
                    'name': tokens[1][1],  # Le nom du curseur
                    'width': int(tokens[3][1]),  # Largeur
                    'height': int(tokens[5][1])  # Hauteur
                }
                print(f"Extracted draw_rectangle data: {command_data}")

            elif tokens[0][1] == 'draw_square' and len(tokens) == 3:
                # Commande draw_square : Nom, taille du côté
                command_data = {
                    'command': 'draw_square',
                    'name': tokens[1][1],  # Le nom du curseur
                    'size': int(tokens[2][1])  # Taille du côté
                }
                print(f"Extracted draw_square data: {command_data}")

            elif tokens[0][1] == 'draw_circle' and len(tokens) == 3:
                # Commande draw_circle : Nom, rayon
                command_data = {
                    'command': 'draw_circle',
                    'name': tokens[1][1],  # Le nom du curseur
                    'radius': int(tokens[2][1])  # Rayon
                }
                print(f"Extracted draw_circle data: {command_data}")

            elif tokens[0][1] == 'draw_arc' and len(tokens) == 5:
                # Commande draw_arc : Nom, rayon, angle de début, angle de fin
                command_data = {
                    'command': 'draw_arc',
                    'name': tokens[1][1],  # Le nom du curseur
                    'radius': int(tokens[2][1]),  # Rayon
                    'start_angle': int(tokens[3][1]),  # Angle de départ
                    'end_angle': int(tokens[4][1])  # Angle de fin
                }
                print(f"Extracted draw_arc data: {command_data}")

            elif tokens[0][1] == 'draw_ellipse' and len(tokens) == 7:
                # Commande draw_ellipse : Nom, dimensions (x, y)
                command_data = {
                    'command': 'draw_ellipse',
                    'name': tokens[1][1],  # Le nom du curseur
                    'width': int(tokens[3][1]),  # Largeur
                    'height': int(tokens[5][1])  # Hauteur
                }
                print(f"Extracted draw_ellipse data: {command_data}")

            elif tokens[0][1] == 'draw_star' and len(tokens) == 4:
                # Commande draw_star : Nom, nombre de branches, taille des branches
                command_data = {
                    'command': 'draw_star',
                    'name': tokens[1][1],  # Le nom du curseur
                    'branches': int(tokens[2][1]),  # Nombre de branches
                    'size': int(tokens[3][1])  # Taille des branches
                }
                print(f"Extracted draw_star data: {command_data}")


            # Ajouter les données extraites à la liste
            if command_data:
                commands_data.append(command_data)
        else:
            print(f"Erreur de syntaxe dans la commande : {error_token}")
    print(f"Commandes extraites : {commands_data}")
    return commands_data


# Fonction pour exécuter les commandes de dessin
def run_draw_commands():
    try:
        current_tab_widget = notebook.nametowidget(notebook.select())  # Onglet actuellement sélectionné
        if current_tab_widget in open_files:
            commands = current_tab_widget.get("1.0", tk.END).strip().splitlines()
            c = analyze_and_extract_commands(commands)
            generate_and_compile (c)
        else:
            tk.messagebox.showerror("Erreur", "Impossible de trouver l'onglet actif pour exécuter les commandes.")
    except Exception as e:
        tk.messagebox.showerror("Erreur",f"Erreur lors de l'exécution : {e}")

# Dictionnaire des commandes de menu
menu_commands = {
    'Fichier': {
        'Nouveau': lambda: create_new_tab(),
        'Ouvrir': open_file,
        'Enregistrer': save_file,
        'Fermer': close_active_tab,
        'Renommer': rename_tab,
        'Quitter': lambda: root.destroy()
    },
    'Édition': {
        'Annuler': undo_action,
        'Répéter': redo_action
    },
    'Luminosité': {
        'Basculer mode': toggle_theme
    },
    'Aide': {
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

run_button = ttk.Button(root, text="Exécuter les commandes", command=run_draw_commands)
root.after(100, position_run_button)  # S'assurer que la fenêtre est prête avant de positionner le bouton

# Créer un premier onglet
create_new_tab()

# Appliquer le thème à tous les onglets existants au démarrage
for file_data in open_files.values():
    if 'text_widget' in file_data and file_data['text_widget'] is not None:
        apply_theme_to_widget(file_data['text_widget'])

# Lancer l'application
root.mainloop()

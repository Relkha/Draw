import tkinter as tk
import cursor_drawing as cd


def execute_all_commands(commands, cursor_manager, drawing_manager):
    """
    Exécute toutes les commandes présentes dans la liste 'commands'.
    La commande sera envoyée à CursorManager si elle correspond à une méthode de ce gestionnaire.
    Sinon, elle sera envoyée à DrawingManager.
    """
    for command in commands:
        parts = command.split()
        if not parts:
            continue  # Ignore les commandes vides

        action = parts[0]  # Premier élément de la commande (par exemple, 'create_cursor')

        # Vérifier si l'action existe dans CursorManager
        if hasattr(cursor_manager, action):
            print(f"Exécution dans CursorManager: {command}")
            cursor_manager.execute_command(command)
        # Si l'action n'existe pas dans CursorManager, essayer avec DrawingManager
        elif len(parts) > 1:  # Si on a plus d'un argument dans la commande
            action = parts[1]  # Essayer à l'index 1
            if hasattr(drawing_manager, action):
                print(f"Exécution dans DrawingManager: {command}")
                drawing_manager.execute_command(command)
        else:
            print(f"Commande non reconnue: {command}")


# Open a drawing window and handle only cursor commands
def open_drawing_window(commands):
    drawing_window = tk.Toplevel()
    drawing_window.title("Cursor Command Window - draw++")
    canvas = tk.Canvas(drawing_window, width=400, height=400, bg="#2e2e2e")  # Dark background
    canvas.pack()

    # Initialize the cursor manager with the canvas
    cursor_manager = cd.CursorManager(canvas)
    drawing_commands = DrawingManager(canvas, cursor_manager)
    execute_all_commands(commands, cursor_manager, drawing_commands)


class DrawingManager:
    def __init__(self, canvas, cursor_manager):
        self.canvas = canvas
        self.cursor_manager = cursor_manager.cursors

    def execute_command(self, command):
        parts = command.split()
        print(f"Exécution de la commande de dessin : {command}")
        if not parts:
            return

        action = parts[1]
        if action == "draw_line" and len(parts) == 3:
            name, _, x = parts
            self.draw_line(name, int(x))

    def draw_line(self, name, x_pixel):
        """Fait avancer le curseur de x_pixel pixels sur l'axe X"""
        if name not in self.cursor_manager:
            print(f"Le curseur {name} n'existe pas.")
            return

        # Récupérer la position actuelle du curseur
        x, y = self.cursor_manager[name]['position']

        # Définir la nouvelle position
        new_x = x + x_pixel  # Avancer de x_pixel pixels sur l'axe X
        self.cursor_manager[name]['position'] = (new_x, y)  # Mettre à jour la position

        # Dessiner la ligne
        self.canvas.create_line(x, y, new_x, y, fill='white', width=2)  # Tracer une ligne horizontale

        # Mettre à jour la position du curseur sur le canvas
        self.canvas.coords(self.cursor_manager[name]['id'], new_x - 5, y - 5, new_x + 5, y + 5)  # Déplacer le curseur
        print(f"Le curseur {name} a été déplacé de {x_pixel} pixels.")

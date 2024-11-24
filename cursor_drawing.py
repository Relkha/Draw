import tkinter as tk


class CursorManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.cursors = {}  # Store cursors by name

    def execute_command(self, command):
        parts = command.split()
        print("im here")
        if not parts:
            return

        action = parts[0]
        if action == "create_cursor" and len(parts) == 5:
            _, name, _, x, y = parts
            self.create_cursor(name, int(x), int(y))

        elif action == "show_cursor" and len(parts) == 2:
            _, name = parts
            self.show_cursor(name)

        elif action == "hide_cursor" and len(parts) == 2:
            _, name = parts
            self.hide_cursor(name)

        elif action == "color_cursor" and len(parts) == 6:
            _, name, _, r, g, b = parts
            self.color_cursor(name, int(r), int(g), int(b))

        elif action == "thickness_cursor" and len(parts) == 4:
            _, name, _, thickness = parts
            self.thickness_cursor(name, int(thickness))

        elif action == "move_cursor" and len(parts) == 5:
            _, name, _, x, y = parts
            self.move_cursor(name, int(x), int(y))

        elif action == "rotate_cursor" and len(parts) == 4:
            _, name, _, angle = parts
            self.rotate_cursor(name, int(angle))

    # Cursor functions updated for dark mode
    def create_cursor(self, name, x, y):
        if name in self.cursors:
            print(f"Le curseur {name} existe déjà.")
            return
        cursor = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#aaaaaa", outline="#aaaaaa", width=1)
        self.cursors[name] = {'id': cursor, 'visible': True, 'angle': 0, 'position': (x, y)}

    def show_cursor(self, name):
        if self._cursor_exists(name):
            self.canvas.itemconfigure(self.cursors[name]['id'], state='normal')

    def hide_cursor(self, name):
        if self._cursor_exists(name):
            self.canvas.itemconfigure(self.cursors[name]['id'], state='hidden')

    def color_cursor(self, name, r, g, b):
        if self._cursor_exists(name):
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.itemconfigure(self.cursors[name]['id'], fill=color, outline=color)

    def thickness_cursor(self, name, thickness):
        if self._cursor_exists(name) and thickness in [1, 2, 3, 4, 5]:
            self.canvas.itemconfigure(self.cursors[name]['id'], width=thickness)

    def move_cursor(self, name, x, y):
        if self._cursor_exists(name):
            cursor = self.cursors[name]
            self.canvas.coords(cursor['id'], x - 5, y - 5, x + 5, y + 5)

    def rotate_cursor(self, name, angle):
        if self._cursor_exists(name):
            self.cursors[name]['angle'] = angle
            print(f"Le curseur {name} a été orienté à {angle} degrés.")

    def _cursor_exists(self, name):
        if name not in self.cursors:
            print(f"Le curseur {name} n'existe pas.")
            return False
        return True


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App with Text Commands")

        # Création du canvas for dark mode
        self.canvas = tk.Canvas(root, width=600, height=400, bg="#2e2e2e")
        self.canvas.pack()

        # Gestionnaire de curseurs
        self.cursor_manager = CursorManager(self.canvas)

        # Zone de texte for dark mode
        self.text_area = Text(root, height=5, bg="#333333", fg="white", insertbackground="white")
        self.text_area.pack(fill='x')

        # Bouton pour exécuter les commandes
        execute_button = tk.Button(root, text="Exécuter Commandes", command=self.execute_commands, bg="#444444",
                                   fg="white")
        execute_button.pack()

    def execute_commands(self):
        commands = self.text_area.get("1.0", tk.END).strip().splitlines()
        for command in commands:
            self.cursor_manager.execute_command(command)
        self.text_area.delete("1.0", tk.END)  # Nettoie la zone de texte après exécution

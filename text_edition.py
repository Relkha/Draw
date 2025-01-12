import tkinter as tk
from tkinter import filedialog, simpledialog, Text, ttk
from analyse_input import process_and_color_line_by_line_with_blocks
from lexer import Lexer
from parser import Parser
from generate_comile_exect_c import generate_and_compile
from autocomplete import Autocomplete
from interactive_doc import open_documentation_window




root = tk.Tk()
root.title("Text Edition - Draw++")
root.geometry("700x500")


notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')


open_files = {}


is_dark_mode = False  


# Function to apply the theme to a specific widget
def apply_theme_to_widget(text_widget):
    if is_dark_mode:
        text_widget.configure(bg="#1e1e1e", fg="white", insertbackground="white")
    else:  # Thème clair
        text_widget.configure(bg="white", fg="black", insertbackground="black")

    configure_tags(text_widget)

def apply_default_tag(text_widget):
    text_widget.tag_add("default", "1.0", "end")

# Function to configure formatting tags
def configure_tags(text_widget):
    if is_dark_mode:
        text_widget.tag_configure("keyword", foreground="cyan", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("conditional", foreground="violet", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("loop", foreground="orange", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("shape", foreground="green", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("function", foreground="pink", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("valid", foreground="white")
        text_widget.tag_configure("incorrect", foreground="red")
        text_widget.tag_configure("default", foreground="white")
    else:
        text_widget.tag_configure("keyword", foreground="blue", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("conditional", foreground="purple", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("loop", foreground="orange", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("shape", foreground="green", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("function", foreground="pink", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("valid", foreground="black")
        text_widget.tag_configure("incorrect", foreground="red")
        text_widget.tag_configure("default", foreground="black")  


def process_and_analyze_without_interference(text_widget):
    current_content = text_widget.get("1.0", "end-1c")
    print(f"[process_and_analyze_without_interference] Before analysis: {current_content}")

    process_and_color_line_by_line_with_blocks(text_widget)
    new_content = text_widget.get("1.0", "end-1c")
    print(f"[process_and_analyze_without_interference] After analysis: {new_content}")

    if current_content != new_content:
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", current_content)
        print("[process_and_analyze_without_interference] Content restored after analysis.")

#Function for tabbed keystrokes
def on_key_release(event, text_widget):
    global open_files

    if text_widget in open_files:
        undo_stack = open_files[text_widget]["undo_stack"]
        redo_stack = open_files[text_widget]["redo_stack"]

        current_content = text_widget.get("1.0", "end-1c")
        if not undo_stack or undo_stack[-1] != current_content:
            undo_stack.append(current_content)
            redo_stack.clear()
            print(f"[on_key_release] Added to undo_stack: {current_content}")

        print(f"[on_key_release] Undo Stack: {undo_stack}")
        print(f"[on_key_release] Redo Stack: {redo_stack}")
        process_and_analyze_without_interference(text_widget)
    else:
        print("[on_key_release] Text widget not found in open_files.")




# Function to create a new tab with a text box
def create_new_tab(title="New File"):
    global open_files

    text_widget = Text(notebook, wrap='word', undo=True, font=("Helvetica", 12), relief="flat", padx=10, pady=10)
    configure_tags(text_widget)

    text_widget.bind("<KeyRelease>", lambda event: on_key_release(event, text_widget))
    notebook.add(text_widget, text=title)
    notebook.select(text_widget)
    open_files[text_widget] = {
        "path": None,
        "undo_stack": [""],
        "redo_stack": []
    }

    print(f"[create_new_tab] Tab created with title: {title}")
    apply_theme_to_widget(text_widget)
    autocomplete = Autocomplete(text_widget)
    autocomplete.enable()
    return text_widget


# Function to close a tab
def close_tab(tab_title):
    if tab_title in open_files:
        current_tab = notebook.index(tab_title)
        notebook.forget(current_tab)
        del open_files[tab_title]

# Function to rename the active tab
def rename_tab():
    current_tab_index = notebook.index("current")
    current_title = notebook.tab(current_tab_index, "text")
    new_title = simpledialog.askstring("Rename tab", "Enter a new name:", initialvalue=current_title)
    if not new_title or new_title.strip() == current_title:
        return
    new_title = new_title.strip()
    if current_title not in open_files:
        open_files[current_title] = {"path": None, "text_widget": None}
    if new_title in open_files:
        tk.messagebox.showerror("Error", f"The tab '{new_title}' already exist.")
        return
    open_files[new_title] = open_files.pop(current_title)
    notebook.tab(current_tab_index, text=new_title)

# Function to open a file
def open_file():
   file_path = filedialog.askopenfilename(defaultextension=".draw", filetypes=[("Draw files", "*.draw"), ("All files", "*.*")])
   if file_path:
        for text_widget, data in open_files.items():
            if data.get("path") == file_path:
                tk.messagebox.showinfo("Info", f"The file '{file_path}' is already open.")
                return 
        file_name = file_path.split('/')[-1]
        with open(file_path, 'r') as file:
            content = file.read()
        text_widget = create_new_tab(file_name)
        text_widget.insert("1.0", content)
        text_widget.edit_modified(False)
        open_files[text_widget] = {
            "path": file_path,
            "undo_stack": [],
            "redo_stack": []
        }
        

# Function to save a file
def save_file():
    current_tab_widget = notebook.nametowidget(notebook.select()) 
    if current_tab_widget in open_files:
        text_widget = current_tab_widget
        content = text_widget.get("1.0", "end-1c")
        file_path = filedialog.asksaveasfilename(defaultextension=".draw", filetypes=[("Draw files", "*.draw"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(content)

            open_files[text_widget]['path'] = file_path

            file_name = file_path.split('/')[-1]
            notebook.tab(current_tab_widget, text=file_name)
    else:
        tk.messagebox.showerror("Error", "No active file found to save.")

# Function to close active tab
def close_active_tab():
    current_tab_index = notebook.index("current")
    if current_tab_index >= 0:
        current_title = notebook.tab(current_tab_index, "text")
        notebook.forget(current_tab_index)
        if current_title in open_files:
            del open_files[current_title]

# Function to cancel the action
def undo_action():
    global open_files

    try:
        current_tab_widget = notebook.nametowidget(notebook.select())
        if current_tab_widget in open_files:
            undo_stack = open_files[current_tab_widget]["undo_stack"]
            redo_stack = open_files[current_tab_widget]["redo_stack"]

            if len(undo_stack) > 1:
                current_content = undo_stack.pop()
                redo_stack.append(current_content)

                previous_content = undo_stack[-1]
                current_tab_widget.delete("1.0", "end")
                current_tab_widget.insert("1.0", previous_content)
                print(f"[undo_action] Undo performed. Undo Stack: {undo_stack}")
                print(f"[undo_action] Redo Stack: {redo_stack}")
            else:
                print("[undo_action] Nothing to undo.")
        else:
            print("[undo_action] No active widget found.")
    except Exception as e:
        print(f"[undo_action] Error: {e}")




# Function to repeat the canceled action
def redo_action():
    global open_files

    try:
        current_tab_widget = notebook.nametowidget(notebook.select())
        if current_tab_widget in open_files:
            undo_stack = open_files[current_tab_widget]["undo_stack"]
            redo_stack = open_files[current_tab_widget]["redo_stack"]

            if redo_stack:
                last_redo = redo_stack.pop()
                undo_stack.append(last_redo)

                current_tab_widget.delete("1.0", "end")
                current_tab_widget.insert("1.0", last_redo)
                print(f"[redo_action] Redo performed. Undo Stack: {undo_stack}")
                print(f"[redo_action] Redo Stack: {redo_stack}")
            else:
                print("[redo_action] Nothing to redo.")
        else:
            print("[redo_action] No active widget found.")
    except Exception as e:
        print(f"[redo_action] Error: {e}")



# Function to switch between dark and bright mode
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode 
    current_tab_widget = notebook.nametowidget(notebook.select()) 
    if current_tab_widget in open_files:
        apply_theme_to_widget(current_tab_widget)
    else:
        tk.messagebox.showerror("Error", "Unable to find the active tab.")

def analyze_and_extract_commands(user_input):
    lines = user_input.splitlines() if isinstance(user_input, str) else user_input
    commands_data = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        condition_type = None 

        if "{" in line:
            block_content = []
            iteration_count = 0
            function_name = ""
            
            if line.startswith("if"):
                condition_type = "if"
                condition_expression = line.split("(", 1)[1].split(")", 1)[0]
            elif line.startswith("else"):
                condition_type = "else"
            elif line.startswith("repeat"):
                iteration_count = int(line.split("(")[1].split(")")[0])
            elif line.startswith("def"):
                function_name = line.split()[1]

            while i < len(lines):
                block_line = lines[i].strip()
                if "}" in block_line:  
                    block_content.append(block_line.split("}")[0].strip())
                    break
                elif "{" not in block_line:
                    block_content.append(block_line)
                i += 1

            block_content_parsed = []
            for block_line in block_content:
                if not block_line:
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

            if condition_type == "if":
                commands_data.append({
                    'command': 'if',
                    'condition': condition_expression,
                    'block': block_content_parsed
                })
            elif condition_type == "else":
                commands_data.append({
                    'command': 'else',
                    'block': block_content_parsed
                })
            elif iteration_count:
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
    Transforms the tokens into a valid command dictionary.
    :param tokens: List of tokens generated by the Lexer.
    :return: A dictionary representing the extracted command.
    """
    command_data = {}

    if tokens[0][1] == 'create_cursor' and len(tokens) == 7:
        command_data = {
            'command': 'create_cursor',
            'name': tokens[1][1],
            'x': (tokens[3][1]),
            'y': (tokens[5][1])
        }
    elif tokens[0][1] == 'move_cursor' and len(tokens) == 7:
        command_data = {
            'command': 'move_cursor',
            'name': tokens[1][1],
            'x': (tokens[3][1]),
            'y': (tokens[5][1])
        }
    elif tokens[0][1] == 'color_cursor' and len(tokens) == 9:
        command_data = {
            'command': 'color_cursor',
            'name': tokens[1][1],
            'r': (tokens[3][1]),
            'g': (tokens[5][1]),
            'b': (tokens[7][1])
        }
    elif tokens[0][1] == 'draw_line' and len(tokens) == 3:
        command_data = {
            'command': 'draw_line',
            'name': tokens[1][1],
            'length': (tokens[2][1])
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
            'angle': (tokens[2][1])
        }
    elif tokens[0][1] == 'thickness_cursor' and len(tokens) == 3:
        command_data = {
            'command': 'thickness_cursor',
            'name': tokens[1][1],
            'thickness': (tokens[2][1])
        }
    elif tokens[0][1] == 'draw_rectangle' and len(tokens) == 7:
        command_data = {
            'command': 'draw_rectangle',
            'name': tokens[1][1],
            'width': (tokens[3][1]),
            'height': (tokens[5][1])
        }
    elif tokens[0][1] == 'draw_square' and len(tokens) == 3:
        command_data = {
            'command': 'draw_square',
            'name': tokens[1][1],
            'size': (tokens[2][1])
        }
    elif tokens[0][1] == 'draw_circle' and len(tokens) == 3:
        command_data = {
            'command': 'draw_circle',
            'name': tokens[1][1],
            'radius': (tokens[2][1])
        }
    elif tokens[0][1] == 'draw_arc' and len(tokens) == 5:
        command_data = {
            'command': 'draw_arc',
            'name': tokens[1][1],
            'radius': (tokens[2][1]),
            'start_angle': (tokens[3][1]),
            'end_angle': (tokens[4][1])
        }
    elif tokens[0][1] == 'draw_ellipse' and len(tokens) == 7:
        command_data = {
            'command': 'draw_ellipse',
            'name': tokens[1][1],
            'width': (tokens[3][1]),
            'height': (tokens[5][1])
        }
    elif tokens[0][1] == 'draw_star' and len(tokens) == 4:
        command_data = {
            'command': 'draw_star',
            'name': tokens[1][1],
            'branches': (tokens[2][1]),
            'size': (tokens[3][1])
        }
    elif tokens[0][1] == 'fill_shape' and len(tokens) == 9:
        command_data = {
            'command': 'fill_shape',
            'name': tokens[1][1],
            'r': (tokens[3][1]),
            'g': (tokens[5][1]),
            'b': (tokens[7][1])
        }
    elif tokens[0][1] == 'var' and len(tokens) == 4:
        command_data = {
            'command': 'var',
            'name': tokens[1][1],
            'value': int(tokens[3][1])
        }
    elif tokens[0][1] == 'if' and len(tokens) >= 4:
        command_data = {
            'command': 'if',
            'condition': tokens[2][1],
            'block': []  
        }
    elif tokens[0][1] == 'else':
        command_data = {
            'command': 'else',
            'block': [] 
        }

        print(f"Erreur : commande non reconnue ou syntaxe incorrecte pour les tokens : {tokens}")

    return command_data



# Function to execute drawing commands
def run_draw_commands():
    try:
        current_tab_widget = notebook.nametowidget(notebook.select())
        if current_tab_widget in open_files:
            commands = current_tab_widget.get("1.0", tk.END).strip().splitlines()
            c = analyze_and_extract_commands(commands)
            generate_and_compile (c)
        else:
            tk.messagebox.showerror("Error", "Unable to find the active tab to execute the commands.")
    except Exception as e:
        tk.messagebox.showerror("Error",f"Error during execution: {e}")


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
        'Documentation': open_documentation_window 
    }
}


menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
for menu_name, commands in menu_commands.items():
    menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=menu_name, menu=menu)
    for command_name, command_func in commands.items():
        menu.add_command(label=command_name, command=command_func)


def position_run_button():
    run_button.place(x=root.winfo_width() - 200, y=10)

run_button = ttk.Button(root, text="Execute commands", command=run_draw_commands)
root.after(100, position_run_button)


create_new_tab()

for file_data in open_files.values():
    if 'text_widget' in file_data and file_data['text_widget'] is not None:
        apply_theme_to_widget(file_data['text_widget'])


root.mainloop()
import os

# Dictionnaire pour stocker les positions des curseurs
cursor_positions = {}

def generate_and_compile(commands_data):
    main_c_code = '''#include <stdio.h>
#include <SDL2/SDL.h>
#include "fonction.c"  // Inclure le fichier fonction.c

int main() {
    initialize_graphics();  // Initialisation de la fenêtre et du renderer
'''

    for command in commands_data:
        if command['command'] == 'create_cursor':
            # Ajout du curseur dans le dictionnaire des positions
            cursor_positions[command['name']] = {'x': command['x'], 'y': command['y']}
            main_c_code += f'    create_cursor("{command["name"]}", {command["x"]}, {command["y"]});\n'
        elif command['command'] == 'move_cursor':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                # Mise à jour de la position dans le dictionnaire
                cursor_positions[command['name']] = {'x': command['x'], 'y': command['y']}
                main_c_code += f'    move_cursor("{command["name"]}", {command["x"]}, {command["y"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")
        elif command['command'] == 'color_cursor':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                # Ajout ou mise à jour de la couleur dans le dictionnaire (si besoin)
                cursor_positions[command['name']]['color'] = {
                    'r': command['r'],
                    'g': command['g'],
                    'b': command['b']
                }
                # Génération du code C
                main_c_code += f'    color_cursor("{command["name"]}", {command["r"]}, {command["g"]}, {command["b"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")
        elif command['command'] == 'draw_line':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                # Génération du code C pour dessiner une ligne
                main_c_code += f'    draw_line("{command["name"]}", {command["length"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")
        elif command['command'] == 'show_cursor':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    show_cursor("{command["name"]}");\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'hide_cursor':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    hide_cursor("{command["name"]}");\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'rotate_cursor':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    rotate_cursor("{command["name"]}", {command["angle"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'thickness_cursor':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    thickness_cursor("{command["name"]}", {command["thickness"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'draw_rectangle':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    draw_rectangle("{command["name"]}", {command["width"]}, {command["height"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'draw_square':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    draw_square("{command["name"]}", {command["size"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'draw_circle':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    draw_circle("{command["name"]}", {command["radius"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'draw_arc':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    draw_arc("{command["name"]}", {command["radius"]}, {command["start_angle"]}, {command["end_angle"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'draw_ellipse':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    draw_ellipse("{command["name"]}", {command["width"]}, {command["height"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")

        elif command['command'] == 'draw_star':
            # Vérifie si le curseur existe déjà
            if command['name'] in cursor_positions:
                main_c_code += f'    draw_star("{command["name"]}", {command["branches"]}, {command["size"]});\n'
            else:
                print(f"Erreur : Le curseur '{command['name']}' n'existe pas. Commande ignorée.")




    main_c_code += '''    SDL_Event event;
    int running = 1;
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = 0;
            }
        }
        SDL_Delay(10);  // Pause pour éviter une boucle trop rapide
    }

    SDL_Quit();
    return 0;
}
'''

    # Écrire le code généré dans le fichier main.c
    with open("main.c", "w") as file:
        file.write(main_c_code)
    print("main.c généré avec succès!")

    # Compiler et exécuter le fichier main.c
    compile_and_run()

def compile_and_run():
    # Compiler le code C
    compilation_result = os.system("gcc main.c -o draw_program -lSDL2 -lm")
    if compilation_result != 0:
        print("Compilation échouée.")
        return

    # Vérifier si l'exécutable a été créé
    if not os.path.exists("./draw_program"):
        print("L'exécutable n'a pas été trouvé.")
        return

    # Exécuter le programme compilé
    execution_result = os.system("./draw_program")
    if execution_result != 0:
        print("Erreur lors de l'exécution du programme.")
    else:
        print("Le programme s'est exécuté avec succès.")

    

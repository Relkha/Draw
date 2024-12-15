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
    compilation_result = os.system("gcc main.c -o draw_program -lSDL2")
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

    

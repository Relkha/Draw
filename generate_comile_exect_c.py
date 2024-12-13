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
            # Déplacer le curseur en fonction de son nom et de ses coordonnées dans le dictionnaire
            if command['name'] in cursor_positions:
                cursor_positions[command['name']]['x'] += command['dx']
                cursor_positions[command['name']]['y'] += command['dy']
            main_c_code += f'    move_cursor("{command["name"]}", {command["dx"]}, {command["dy"]});\n'
        elif command['command'] == 'color_cursor':
            main_c_code += f'    color_cursor("{command["name"]}", {command["r"]}, {command["g"]}, {command["b"]});\n'

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

    

#include <stdio.h>
#include <SDL2/SDL.h>
#include "fonction.c"  // Inclure le fichier fonction.c

int main() {
    initialize_graphics();  // Initialisation de la fenêtre et du renderer
    create_cursor("c", 150, 100);
    create_cursor("curseur", 150, 250);
    color_cursor("c", 140, 140, 140);
    color_cursor("curseur", 200, 140, 200);
    SDL_Event event;
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

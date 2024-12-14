#include <stdio.h>
#include <SDL2/SDL.h>
#include "fonction.c"  // Inclure le fichier fonction.c

int main() {
    initialize_graphics();  // Initialisation de la fenêtre et du renderer
    create_cursor("C", 100, 200);
    move_cursor("C", 350, 120);
    color_cursor("C", 255, 25, 20);
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

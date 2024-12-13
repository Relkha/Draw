#include <SDL2/SDL.h>
#include <stdio.h>

// Définir une taille pour le curseur (un petit carré)
#define CURSOR_SIZE 1

// Déclaration des variables globales de la fenêtre et du renderer
SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;
// Structure pour stocker les informations d'un curseur
// Structure pour stocker les informations d'un curseur
typedef struct {
    const char *name;
    int x;
    int y;
} Cursor;

// Tableau pour stocker jusqu'à 10 curseurs
Cursor cursors[CURSOR_SIZE];

// Fonction pour initialiser SDL2 et la fenêtre
void initialize_graphics() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return;
    }

    // Créer la fenêtre principale
    window = SDL_CreateWindow("Drawing Window", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 600, 400, SDL_WINDOW_SHOWN);
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    if (!window) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return;
    }

    // Créer le renderer
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        return;
    }
}

// Fonction pour créer un curseur
void create_cursor(const char *name, int x, int y) {
    // Ici, on ne garde pas nécessairement une structure, on pourrait afficher directement le curseur
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);  // Noir par défaut
    SDL_Rect cursor = {x - CURSOR_SIZE / 2, y - CURSOR_SIZE / 2, CURSOR_SIZE, CURSOR_SIZE};
    SDL_RenderFillRect(renderer, &cursor);
    SDL_RenderPresent(renderer);
    printf("Le curseur %s a été créé aux coordonnées (%d, %d)\n", name, x, y);
}

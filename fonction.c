#include <SDL2/SDL.h>
#include <stdio.h>
#include <string.h>

#define CURSOR_SIZE 10  // Taille du curseur
#define MAX_CURSORS 100 // Nombre maximum de curseurs

// Structures SDL pour la fenêtre et le renderer
SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;

// Structure pour représenter un curseur
typedef struct {
    char name[50]; // Nom du curseur
    int x;         // Coordonnée X
    int y;         // Coordonnée Y
    int r;         // Composante Rouge
    int g;         // Composante Verte
    int b;         // Composante Bleue
} Cursor;

// Tableau pour stocker les curseurs
Cursor cursors[MAX_CURSORS];
int cursor_count = 0;

// Fonction pour initialiser SDL et créer une fenêtre
void initialize_graphics() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return;
    }

    window = SDL_CreateWindow("Drawing Window", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 600, 400, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_Quit();
        return;
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return;
    }

    // Remplir le fond en blanc
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Blanc
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);

    printf("Graphiques initialisés avec succès.\n");
}


// Fonction pour créer un curseur
void create_cursor(const char *name, int x, int y) {
    // Vérifie les coordonnées
    if (x < 0 || y < 0 || x >= 600 || y >= 400) {
        printf("Erreur : Les coordonnées (%d, %d) sont hors de la fenêtre.\n", x, y);
        return;
    }

    // Vérifie si un curseur avec le même nom existe déjà
    for (int i = 0; i < cursor_count; i++) {
        if (strcmp(cursors[i].name, name) == 0) {
            printf("Erreur : Un curseur avec le nom '%s' existe déjà.\n", name);
            return;
        }
    }

    // Ajoute un nouveau curseur
    if (cursor_count >= MAX_CURSORS) {
        printf("Erreur : Nombre maximum de curseurs atteint (%d).\n", MAX_CURSORS);
        return;
    }

    strncpy(cursors[cursor_count].name, name, sizeof(cursors[cursor_count].name) - 1);
    cursors[cursor_count].x = x;
    cursors[cursor_count].y = y;
    cursors[cursor_count].r = 0; // Couleur par défaut : noir
    cursors[cursor_count].g = 0;
    cursors[cursor_count].b = 0;
    cursor_count++;

    redraw_all_cursors();
    printf("Curseur '%s' créé aux coordonnées (%d, %d).\n", name, x, y);
}



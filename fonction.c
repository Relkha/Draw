#include <SDL2/SDL.h>
#include <stdio.h>
#include <string.h>
#include <math.h> // Pour cos() et sin()

#define MAX_CURSORS 100
#define MAX_LINES 100
#define PI 3.14159265358979323846

typedef struct {
    char name[50];
    int x, y;         // Position
    int r, g, b;      // Couleur
    int thickness;    // Épaisseur
    int visible;      // Visibilité
    float angle;      // Orientation en degrés
} Cursor;

typedef struct {
    int x_start, y_start;
    int x_end, y_end;
    int r, g, b;      // Couleur de la ligne
} Line;

Cursor cursors[MAX_CURSORS];
Line lines[MAX_LINES];  // Tableau pour stocker les lignes dessinées
int cursor_count = 0;
int line_count = 0;      // Nombre de lignes dessinées

// SDL Renderer et Window
SDL_Window* window = NULL;
SDL_Renderer* renderer = NULL;

// Initialisation SDL
int initialize_graphics() {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("Erreur d'initialisation SDL : %s\n", SDL_GetError());
        return 0;
    }
    window = SDL_CreateWindow("Dessin avec curseurs", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Erreur de création de fenêtre : %s\n", SDL_GetError());
        SDL_Quit();
        return 0;
    }
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) {
        printf("Erreur de création de renderer : %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 0;
    }
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
    return 1;
}

// Fonction utilitaire pour trouver un curseur par nom
Cursor* find_cursor(const char* name) {
    for (int i = 0; i < cursor_count; i++) {
        if (strcmp(cursors[i].name, name) == 0) {
            return &cursors[i];
        }
    }
    return NULL;
}

void update_screen() {
    // Effacer l'écran (fond blanc)
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // Fond blanc
    SDL_RenderClear(renderer); 

    // Dessiner toutes les lignes stockées
    for (int i = 0; i < line_count; i++) {
        SDL_SetRenderDrawColor(renderer, lines[i].r, lines[i].g, lines[i].b, 255);
        SDL_RenderDrawLine(renderer, lines[i].x_start, lines[i].y_start, lines[i].x_end, lines[i].y_end);
    }

    // Dessiner les curseurs
    for (int i = 0; i < cursor_count; i++) {
        if (cursors[i].visible) {
            SDL_SetRenderDrawColor(renderer, cursors[i].r, cursors[i].g, cursors[i].b, 255);
            SDL_Rect rect = { cursors[i].x - 5, cursors[i].y - 5, 10, 10 };
            SDL_RenderFillRect(renderer, &rect);
        }
    }

    // Afficher le rendu final
    SDL_RenderPresent(renderer);
}


// Création d'un curseur
void create_cursor(const char* name, int x, int y) {
    if (cursor_count >= MAX_CURSORS) {
        printf("Erreur : Nombre maximal de curseurs atteint.\n");
        return;
    }

    Cursor new_cursor;
    strncpy(new_cursor.name, name, sizeof(new_cursor.name) - 1);
    new_cursor.x = x;
    new_cursor.y = y;
    new_cursor.r = 0;
    new_cursor.g = 0;
    new_cursor.b = 0;
    new_cursor.thickness = 1;
    new_cursor.visible = 1;
    new_cursor.angle = 0.0; // Angle initial = 0° (orienté vers la droite)

    cursors[cursor_count++] = new_cursor;

    printf("Curseur %s créé en position (%d, %d).\n", name, x, y);
    update_screen();
}

// Changer la couleur d'un curseur
void color_cursor(const char* name, int r, int g, int b) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    cursor->r = r;
    cursor->g = g;
    cursor->b = b;

    printf("Couleur du curseur %s changée en (%d, %d, %d).\n", name, r, g, b);
}

void draw_line(const char* name, int length) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    // Coordonnées de départ
    int x_start = cursor->x;
    int y_start = cursor->y;

    // Conversion de l'angle en radians
    float angle_rad = cursor->angle * (PI / 180.0);

    // Calcul des nouvelles coordonnées en fonction de l'angle
    int x_end = x_start + (int)(cos(angle_rad) * length);
    int y_end = y_start - (int)(sin(angle_rad) * length);

    // Ajouter la ligne au tableau
    if (line_count < MAX_LINES) {
        lines[line_count++] = (Line){x_start, y_start, x_end, y_end, cursor->r, cursor->g, cursor->b};
    } else {
        printf("Erreur : Nombre maximal de lignes atteint.\n");
    }

    // Mise à jour des coordonnées du curseur
    cursor->x = x_end;
    cursor->y = y_end;

    // Mise à jour de l'écran
    update_screen();

    printf("Ligne dessinée depuis (%d, %d) jusqu'à (%d, %d).\n", x_start, y_start, x_end, y_end);
}

// Afficher un curseur
void show_cursor(const char* name) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }
    cursor->visible = 1;
    printf("Curseur %s affiché.\n", name);
    update_screen();
}

// Cacher un curseur
void hide_cursor(const char* name) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }
    cursor->visible = 0;
    printf("Curseur %s caché.\n", name);
    update_screen();
}

// Déplacer un curseur
void move_cursor(const char* name, int x, int y) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }
    cursor->x = x;
    cursor->y = y;
    printf("Curseur %s déplacé à (%d, %d).\n", name, x, y);
    update_screen();
}

// Tourner un curseur
void rotate_cursor(const char* name, int angle) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }
    cursor->angle += angle;
    printf("Curseur %s tourné de %d°.\n", name, angle);
}

// Modifier l'épaisseur des traits d'un curseur
void thickness_cursor(const char* name, int thickness) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }
    cursor->thickness = thickness;
    printf("Épaisseur du curseur %s définie à %d.\n", name, thickness);
}

// Dessiner un rectangle
void draw_rectangle(const char* name, int width, int height) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    int x = cursor->x;
    int y = cursor->y;

    // Lignes du rectangle
    draw_line(name, width);
    rotate_cursor(name, 90);
    draw_line(name, height);
    rotate_cursor(name, 90);
    draw_line(name, width);
    rotate_cursor(name, 90);
    draw_line(name, height);
    rotate_cursor(name, 90);

    cursor->x = x; // Revenir à la position de départ
    cursor->y = y;
}

// Dessiner un carré
void draw_square(const char* name, int size) {
    draw_rectangle(name, size, size);
}

// Dessiner un cercle
void draw_circle(const char* name, int radius) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    for (int angle = 0; angle < 360; angle++) {
        int x = cursor->x + radius * cos(angle * PI / 180.0);
        int y = cursor->y - radius * sin(angle * PI / 180.0);
        SDL_SetRenderDrawColor(renderer, cursor->r, cursor->g, cursor->b, 255);
        SDL_RenderDrawPoint(renderer, x, y);
    }
    SDL_RenderPresent(renderer);
    printf("Cercle dessiné avec un rayon de %d.\n", radius);
}

// Dessiner un arc
void draw_arc(const char* name, int radius, int start_angle, int end_angle) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    float angle_step = 1.0; 
    for (float angle = start_angle; angle <= end_angle; angle += angle_step) {
        int x = cursor->x + (int)(radius * cos(angle * PI / 180.0));
        int y = cursor->y - (int)(radius * sin(angle * PI / 180.0));
        SDL_SetRenderDrawColor(renderer, cursor->r, cursor->g, cursor->b, 255);
        SDL_RenderDrawPoint(renderer, x, y);
    }
    SDL_RenderPresent(renderer);
}

// Dessiner une ellipse
void draw_ellipse(const char* name, int width, int height) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    for (int angle = 0; angle < 360; angle++) {
        int x = cursor->x + width * cos(angle * PI / 180.0);
        int y = cursor->y - height * sin(angle * PI / 180.0);
        SDL_SetRenderDrawColor(renderer, cursor->r, cursor->g, cursor->b, 255);
        SDL_RenderDrawPoint(renderer, x, y);
    }
    SDL_RenderPresent(renderer);
    printf("Ellipse dessinée avec largeur %d et hauteur %d.\n", width, height);
}

// Dessiner une étoile
void draw_star(const char* name, int branches, int size) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    double angle_step = PI / branches;
    int x_center = cursor->x;
    int y_center = cursor->y;

    int x_prev = x_center + size * cos(0);
    int y_prev = y_center - size * sin(0);

    for (int i = 1; i <= 2 * branches; i++) {
        double angle = i * angle_step;
        int length = (i % 2 == 0) ? size : size / 2;
        int x_next = x_center + length * cos(angle);
        int y_next = y_center - length * sin(angle);

        SDL_SetRenderDrawColor(renderer, cursor->r, cursor->g, cursor->b, 255);
        SDL_RenderDrawLine(renderer, x_prev, y_prev, x_next, y_next);

        x_prev = x_next;
        y_prev = y_next;
    }

    SDL_RenderPresent(renderer);
}




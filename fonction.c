#include <SDL2/SDL.h>
#include <stdio.h>
#include <string.h>
#include <math.h> // Pour cos() et sin()

#define MAX_CURSORS 100
#define MAX_LINES 100
#define PI 3.14159265358979323846
#define MAX_SHAPES 100

typedef enum {
    SHAPE_CIRCLE,
    SHAPE_ELLIPSE,
    SHAPE_ARC,
    SHAPE_STAR
} ShapeType;

typedef struct {
    ShapeType type;
    int x, y;         // Position du centre
    int param1, param2; // Paramètres spécifiques (rayon, largeur, hauteur, etc.)
    int start_angle, end_angle; // Angles pour les arcs
    int r, g, b;      // Couleur
    int branches;     // Branches (étoiles uniquement)
} Shape;

Shape shapes[MAX_SHAPES];
int shape_count = 0;


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
    int r, g, b;    // Couleur de la ligne
    int thickness;
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
    // Effacer l'écran avec un fond blanc
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer);

    // Dessiner toutes les lignes stockées avec une largeur réduite et centrée
    for (int i = 0; i < line_count; i++) {
        SDL_SetRenderDrawColor(renderer, lines[i].r, lines[i].g, lines[i].b, 255);

        // Réduire la largeur de la ligne pour qu'elle reste petite
        int reduced_thickness = lines[i].thickness / 5;
        int half_reduced_thickness = reduced_thickness / 2;

        if (lines[i].x_start == lines[i].x_end) {
            // Ligne verticale centrée
            SDL_Rect rect = {
                lines[i].x_start - half_reduced_thickness, 
                (lines[i].y_start < lines[i].y_end ? lines[i].y_start : lines[i].y_end),
                reduced_thickness, // Largeur réduite
                abs(lines[i].y_end - lines[i].y_start)
            };
            SDL_RenderFillRect(renderer, &rect);
        } else if (lines[i].y_start == lines[i].y_end) {
            // Ligne horizontale centrée
            SDL_Rect rect = {
                (lines[i].x_start < lines[i].x_end ? lines[i].x_start : lines[i].x_end),
                lines[i].y_start - half_reduced_thickness, // Centrer verticalement
                abs(lines[i].x_end - lines[i].x_start),
                reduced_thickness // Hauteur réduite
            };
            SDL_RenderFillRect(renderer, &rect);
        } else {
            // Ligne inclinée (approximation par points avec largeur réduite et centrée)
            float dx = lines[i].x_end - lines[i].x_start;
            float dy = lines[i].y_end - lines[i].y_start;
            float length = sqrt(dx * dx + dy * dy);
            float ux = dx / length, uy = dy / length;

            for (int offset = -half_reduced_thickness; offset <= half_reduced_thickness; offset++) {
                for (int j = 0; j < length; j++) {
                    int x = lines[i].x_start + j * ux - offset * uy;
                    int y = lines[i].y_start + j * uy + offset * ux;
                    SDL_RenderDrawPoint(renderer, x, y);
                }
            }
        }
    }

    // Dessiner tous les curseurs visibles
    for (int i = 0; i < cursor_count; i++) {
        if (cursors[i].visible) {
            // Dessiner le curseur lui-même
            SDL_SetRenderDrawColor(renderer, cursors[i].r, cursors[i].g, cursors[i].b, 255);
            SDL_Rect rect = {
                cursors[i].x - cursors[i].thickness / 2, 
                cursors[i].y - cursors[i].thickness / 2, 
                cursors[i].thickness, 
                cursors[i].thickness
            };
            SDL_RenderFillRect(renderer, &rect);
        }
    }

    // Dessiner toutes les formes géométriques stockées
    for (int i = 0; i < shape_count; i++) {
        SDL_SetRenderDrawColor(renderer, shapes[i].r, shapes[i].g, shapes[i].b, 255);
        switch (shapes[i].type) {
            case SHAPE_CIRCLE:
                for (int angle = 0; angle < 360; angle++) {
                    int x = shapes[i].x + shapes[i].param1 * cos(angle * PI / 180.0);
                    int y = shapes[i].y - shapes[i].param1 * sin(angle * PI / 180.0);
                    SDL_RenderDrawPoint(renderer, x, y);
                }
                break;

            case SHAPE_ARC:
                for (int angle = shapes[i].start_angle; angle <= shapes[i].end_angle; angle++) {
                    int x = shapes[i].x + shapes[i].param1 * cos(angle * PI / 180.0);
                    int y = shapes[i].y - shapes[i].param1 * sin(angle * PI / 180.0);
                    SDL_RenderDrawPoint(renderer, x, y);
                }
                break;

            case SHAPE_ELLIPSE:
                for (int angle = 0; angle < 360; angle++) {
                    int x = shapes[i].x + shapes[i].param1 * cos(angle * PI / 180.0);
                    int y = shapes[i].y - shapes[i].param2 * sin(angle * PI / 180.0);
                    SDL_RenderDrawPoint(renderer, x, y);
                }
                break;

            case SHAPE_STAR:
                {
                    double angle_step = PI / shapes[i].branches;
                    int x_center = shapes[i].x;
                    int y_center = shapes[i].y;

                    int x_prev = x_center + shapes[i].param1 * cos(0);
                    int y_prev = y_center - shapes[i].param1 * sin(0);

                    for (int j = 1; j <= 2 * shapes[i].branches; j++) {
                        double angle = j * angle_step;
                        int length = (j % 2 == 0) ? shapes[i].param1 : shapes[i].param1 / 2;
                        int x_next = x_center + length * cos(angle);
                        int y_next = y_center - length * sin(angle);

                        SDL_RenderDrawLine(renderer, x_prev, y_prev, x_next, y_next);

                        x_prev = x_next;
                        y_prev = y_next;
                    }
                }
                break;
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
    new_cursor.thickness = 10;
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

    // Ajouter la ligne au tableau avec l'épaisseur du curseur
    if (line_count < MAX_LINES) {
        lines[line_count++] = (Line){x_start, y_start, x_end, y_end, cursor->r, cursor->g, cursor->b, cursor->thickness};
    } else {
        printf("Erreur : Nombre maximal de lignes atteint.\n");
    }

    // Mise à jour des coordonnées du curseur
    cursor->x = x_end;
    cursor->y = y_end;

    // Mise à jour de l'écran
    update_screen();

    printf("Ligne dessinée depuis (%d, %d) jusqu'à (%d, %d), épaisseur : %d.\n", x_start, y_start, x_end, y_end, cursor->thickness);
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
    update_screen();
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

    // Ajouter le cercle au tableau
    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){SHAPE_CIRCLE, cursor->x, cursor->y, radius, 0, 0, 0, cursor->r, cursor->g, cursor->b, 0};
    } else {
        printf("Erreur : Nombre maximal de formes atteint.\n");
    }

    update_screen(); // Redessiner tout
    printf("Cercle ajouté avec un rayon de %d.\n", radius);
}

// Dessiner un arc
void draw_arc(const char* name, int radius, int start_angle, int end_angle) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    // Ajouter l'arc au tableau
    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){SHAPE_ARC, cursor->x, cursor->y, radius, 0, start_angle, end_angle, cursor->r, cursor->g, cursor->b, 0};
    } else {
        printf("Erreur : Nombre maximal de formes atteint.\n");
    }

    update_screen(); // Redessiner tout
    printf("Arc ajouté avec un rayon de %d, de %d° à %d°.\n", radius, start_angle, end_angle);
}


// Dessiner une ellipse
void draw_ellipse(const char* name, int width, int height) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    // Ajouter l'ellipse au tableau
    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){
            SHAPE_ELLIPSE,    // Type de la forme
            cursor->x,        // Position du centre
            cursor->y,        // Position du centre
            width,            // Largeur (rayon horizontal)
            height,           // Hauteur (rayon vertical)
            0,                // Début d'angle inutilisé
            0,                // Fin d'angle inutilisé
            cursor->r,        // Couleur rouge
            cursor->g,        // Couleur verte
            cursor->b,        // Couleur bleue
            0                 // Branches inutilisé
        };
    } else {
        printf("Erreur : Nombre maximal de formes atteint.\n");
        return;
    }

    update_screen(); // Redessiner tout
    printf("Ellipse ajoutée avec largeur %d et hauteur %d.\n", width, height);
}

// Dessiner une étoile
void draw_star(const char* name, int branches, int size) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Erreur : Curseur %s non trouvé.\n", name);
        return;
    }

    // Ajouter l'étoile au tableau
    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){
            SHAPE_STAR,       // Type de la forme
            cursor->x,        // Position du centre
            cursor->y,        // Position du centre
            size,             // Taille (longueur des branches)
            0,                // Paramètre inutilisé
            0,                // Début d'angle inutilisé
            0,                // Fin d'angle inutilisé
            cursor->r,        // Couleur rouge
            cursor->g,        // Couleur verte
            cursor->b,        // Couleur bleue
            branches          // Nombre de branches
        };
    } else {
        printf("Erreur : Nombre maximal de formes atteint.\n");
        return;
    }

    update_screen(); // Redessiner tout
    printf("Étoile ajoutée avec %d branches et taille %d.\n", branches, size);
}





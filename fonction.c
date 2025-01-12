// A program using SDL2 for creating cursors, drawing lines, and rendering geometric shapes.
#include <SDL2/SDL.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

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
    int x, y;
    int param1, param2;
    int start_angle, end_angle;
    int r, g, b;
    int branches;
} Shape;

Shape shapes[MAX_SHAPES];
int shape_count = 0;

typedef struct {
    char name[50];
    int x, y;
    int r, g, b;
    int thickness;
    int visible;
    float angle;
} Cursor;

typedef struct {
    int x_start, y_start;
    int x_end, y_end;
    int r, g, b;
    int thickness;
} Line;

Cursor cursors[MAX_CURSORS];
Line lines[MAX_LINES];
int cursor_count = 0;
int line_count = 0;

SDL_Window* window = NULL;
SDL_Renderer* renderer = NULL;

// Initializes SDL and creates a window and renderer
int initialize_graphics() {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("SDL initialization error: %s\n", SDL_GetError());
        return 0;
    }
    window = SDL_CreateWindow("Drawing with Cursors", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Window creation error: %s\n", SDL_GetError());
        SDL_Quit();
        return 0;
    }
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) {
        printf("Renderer creation error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 0;
    }
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
    return 1;
}

// Finds a cursor by its name
Cursor* find_cursor(const char* name) {
    for (int i = 0; i < cursor_count; i++) {
        if (strcmp(cursors[i].name, name) == 0) {
            return &cursors[i];
        }
    }
    return NULL;
}

// Updates the screen by rendering all shapes, lines, and visible cursors
void update_screen() {
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer);

    for (int i = 0; i < line_count; i++) {
        SDL_SetRenderDrawColor(renderer, lines[i].r, lines[i].g, lines[i].b, 255);
        int reduced_thickness = lines[i].thickness / 5;
        int half_reduced_thickness = reduced_thickness / 2;

        if (lines[i].x_start == lines[i].x_end) {
            SDL_Rect rect = {
                lines[i].x_start - half_reduced_thickness, 
                (lines[i].y_start < lines[i].y_end ? lines[i].y_start : lines[i].y_end),
                reduced_thickness,
                abs(lines[i].y_end - lines[i].y_start)
            };
            SDL_RenderFillRect(renderer, &rect);
        } else if (lines[i].y_start == lines[i].y_end) {
            SDL_Rect rect = {
                (lines[i].x_start < lines[i].x_end ? lines[i].x_start : lines[i].x_end),
                lines[i].y_start - half_reduced_thickness,
                abs(lines[i].x_end - lines[i].x_start),
                reduced_thickness
            };
            SDL_RenderFillRect(renderer, &rect);
        } else {
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

    for (int i = 0; i < cursor_count; i++) {
        if (cursors[i].visible) {
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
            case SHAPE_STAR: {
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

    SDL_RenderPresent(renderer);
}

// Creates a new cursor at the given position
void create_cursor(const char* name, int x, int y) {
    if (cursor_count >= MAX_CURSORS) {
        printf("Error: Maximum number of cursors reached.\n");
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
    new_cursor.angle = 0.0;

    cursors[cursor_count++] = new_cursor;

    printf("Cursor %s created at position (%d, %d).\n", name, x, y);
    update_screen();
}

// Changes the color of a cursor
void color_cursor(const char* name, int r, int g, int b) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }
    cursor->r = r;
    cursor->g = g;
    cursor->b = b;

    printf("Cursor %s color changed to (%d, %d, %d).\n", name, r, g, b);
}

// Draws a line from the current cursor position
void draw_line(const char* name, int length) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }
    int x_start = cursor->x;
    int y_start = cursor->y;

    float angle_rad = cursor->angle * (PI / 180.0);

    int x_end = x_start + (int)(cos(angle_rad) * length);
    int y_end = y_start - (int)(sin(angle_rad) * length);

    if (line_count < MAX_LINES) {
        lines[line_count++] = (Line){x_start, y_start, x_end, y_end, cursor->r, cursor->g, cursor->b, cursor->thickness};
    } else {
        printf("Error: Maximum number of lines reached.\n");
    }

    cursor->x = x_end;
    cursor->y = y_end;
    update_screen();

    printf("Line drawn from (%d, %d) to (%d, %d), thickness: %d.\n", x_start, y_start, x_end, y_end, cursor->thickness);
}

// Shows a cursor
void show_cursor(const char* name) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }
    cursor->visible = 1;
    printf("Cursor %s is now visible.\n", name);
    update_screen();
}

// Hides a cursor
void hide_cursor(const char* name) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }
    cursor->visible = 0;
    printf("Cursor %s is now hidden.\n", name);
    update_screen();
}

// Moves a cursor to a new position
void move_cursor(const char* name, int x, int y) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }
    cursor->x = x;
    cursor->y = y;
    printf("Cursor %s moved to (%d, %d).\n", name, x, y);
    update_screen();
}

// Rotates a cursor by a given angle
void rotate_cursor(const char* name, int angle) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }
    cursor->angle += angle;
    printf("Cursor %s rotated by %d degrees.\n", name, angle);
}

// Sets the thickness of a cursor's lines
void thickness_cursor(const char* name, int thickness) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }
    cursor->thickness = thickness;
    printf("Cursor %s thickness set to %d.\n", name, thickness);
    update_screen();
}

// Draws a rectangle from the cursor's position
void draw_rectangle(const char* name, int width, int height) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }

    int x = cursor->x;
    int y = cursor->y;

    draw_line(name, width);
    rotate_cursor(name, 90);
    draw_line(name, height);
    rotate_cursor(name, 90);
    draw_line(name, width);
    rotate_cursor(name, 90);
    draw_line(name, height);
    rotate_cursor(name, 90);

    cursor->x = x;
    cursor->y = y;
}

// Draws a square from the cursor's position
void draw_square(const char* name, int size) {
    draw_rectangle(name, size, size);
}

// Draws a circle at the cursor's position
void draw_circle(const char* name, int radius) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }

    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){SHAPE_CIRCLE, cursor->x, cursor->y, radius, 0, 0, 0, cursor->r, cursor->g, cursor->b, 0};
    } else {
        printf("Error: Maximum number of shapes reached.\n");
    }

    update_screen();
    printf("Circle added with radius %d.\n", radius);
}

// Draws an arc at the cursor's position
void draw_arc(const char* name, int radius, int start_angle, int end_angle) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }

    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){SHAPE_ARC, cursor->x, cursor->y, radius, 0, start_angle, end_angle, cursor->r, cursor->g, cursor->b, 0};
    } else {
        printf("Error: Maximum number of shapes reached.\n");
    }

    update_screen();
    printf("Arc added with radius %d, from %d to %d degrees.\n", radius, start_angle, end_angle);
}

// Draws an ellipse at the cursor's position
void draw_ellipse(const char* name, int width, int height) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }

    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){SHAPE_ELLIPSE, cursor->x, cursor->y, width, height, 0, 0, cursor->r, cursor->g, cursor->b, 0};
    } else {
        printf("Error: Maximum number of shapes reached.\n");
        return;
    }

    update_screen();
    printf("Ellipse added with width %d and height %d.\n", width, height);
}

// Draws a star at the cursor's position
void draw_star(const char* name, int branches, int size) {
    Cursor* cursor = find_cursor(name);
    if (!cursor) {
        printf("Error: Cursor %s not found.\n", name);
        return;
    }

    if (shape_count < MAX_SHAPES) {
        shapes[shape_count++] = (Shape){SHAPE_STAR, cursor->x, cursor->y, size, 0, 0, 0, cursor->r, cursor->g, cursor->b, branches};
    } else {
        printf("Error: Maximum number of shapes reached.\n");
        return;
    }

    update_screen();
    printf("Star added with %d branches and size %d.\n", branches, size);
}

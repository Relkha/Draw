# A Python script for generating, compiling, and executing C code based on user-defined commands
import os

# Dictionary to store cursor positions
cursor_positions = {}

# Generates C code for a specific command
def generate_command_code(command):
    if command['command'] == 'create_cursor':
        return f'create_cursor("{command["name"]}", {command["x"]}, {command["y"]});'
    elif command['command'] == 'move_cursor':
        return f'move_cursor("{command["name"]}", {command["x"]}, {command["y"]});'
    elif command['command'] == 'color_cursor':
        return f'color_cursor("{command["name"]}", {command["r"]}, {command["g"]}, {command["b"]});'
    elif command['command'] == 'draw_line':
        return f'draw_line("{command["name"]}", {command["length"]});'
    elif command['command'] == 'show_cursor':
        return f'show_cursor("{command["name"]}");'
    elif command['command'] == 'hide_cursor':
        return f'hide_cursor("{command["name"]}");'
    elif command['command'] == 'rotate_cursor':
        return f'rotate_cursor("{command["name"]}", {command["angle"]});'
    elif command['command'] == 'thickness_cursor':
        return f'thickness_cursor("{command["name"]}", {command["thickness"]});'
    elif command['command'] == 'draw_rectangle':
        return f'draw_rectangle("{command["name"]}", {command["width"]}, {command["height"]});'
    elif command['command'] == 'draw_square':
        return f'draw_square("{command["name"]}", {command["size"]});'
    elif command['command'] == 'draw_circle':
        return f'draw_circle("{command["name"]}", {command["radius"]});'
    elif command['command'] == 'draw_arc':
        return f'draw_arc("{command["name"]}", {command["radius"]}, {command["start_angle"]}, {command["end_angle"]});'
    elif command['command'] == 'draw_ellipse':
        return f'draw_ellipse("{command["name"]}", {command["width"]}, {command["height"]});'
    elif command['command'] == 'draw_star':
        return f'draw_star("{command["name"]}", {command["branches"]}, {command["size"]});'
    elif command['command'] == 'var':
        return f'int {command["name"]} = {command["value"]};'
    else:
        return None

# Generates and compiles the main.c file based on commands
def generate_and_compile(commands_data):
    main_c_code = '''#include <stdio.h>
#include <SDL2/SDL.h>
#include "fonction.c"  // Include the external functions file

int main() {
    initialize_graphics();
'''

    for command in commands_data:
        if command['command'] == 'repeat':
            main_c_code += f'    for (int i = 0; i < {command["iterations"]}; i++) {{\n'
            for sub_command in command['block']:
                generated_code = generate_command_code(sub_command)
                if generated_code:
                    main_c_code += f'        {generated_code}\n'
            main_c_code += '    }\n'
        elif command['command'] == 'if':
            main_c_code += f'    if ({command["condition"]}) {{\n'
            for sub_command in command['block']:
                generated_code = generate_command_code(sub_command)
                if generated_code:
                    main_c_code += f'        {generated_code}\n'
            main_c_code += '    }\n'
        elif command['command'] == 'else':
            main_c_code += '    else {\n'
            for sub_command in command['block']:
                generated_code = generate_command_code(sub_command)
                if generated_code:
                    main_c_code += f'        {generated_code}\n'
            main_c_code += '    }\n'
        elif command['command'] == 'def':
            function_code = f'void {command["name"]}() {{\n'
            for sub_command in command['block']:
                generated_code = generate_command_code(sub_command)
                if generated_code:
                    function_code += f'    {generated_code}\n'
            function_code += '}\n'
            prepend_code_to_main(function_code)
        else:
            generated_code = generate_command_code(command)
            if generated_code:
                main_c_code += f'    {generated_code}\n'

    main_c_code += '''    SDL_Event event;
    int running = 1;
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = 0;
            }
        }
        SDL_Delay(10);
    }

    SDL_Quit();
    return 0;
}
'''

    with open("main.c", "w") as file:
        file.write(main_c_code)
    print("main.c generated successfully!")

    compile_and_run()

# Prepends additional code to main.c
def prepend_code_to_main(code):
    with open("main.c", "r") as file:
        content = file.read()
    with open("main.c", "w") as file:
        file.write(code + "\n" + content)

# Compiles and runs the generated C code
def compile_and_run():
    compilation_result = os.system("gcc main.c -o draw_program -lSDL2 -lm")
    if compilation_result != 0:
        print("Compilation failed.")
        return

    if not os.path.exists("./draw_program"):
        print("Executable not found.")
        return

    execution_result = os.system("./draw_program")
    if execution_result != 0:
        print("Program execution error.")
    else:
        print("Program executed successfully.")

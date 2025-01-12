# This script analyzes and tags lines of code, line by line, or entire code blocks, applying syntax highlighting or error marking.
# It uses a Lexer for tokenization and a Parser for syntax validation.

from lexer import Lexer
from parser import Parser


def process_and_color_line_by_line_with_blocks(text_widget):
    """
    Analyzes the content line by line and processes complete blocks.
    """
    # Retrieve the content of the text widget
    content = text_widget.get("1.0", "end-1c")
    lines = content.splitlines()
    inside_block = False
    block_lines = []
    block_start_line = 0

    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        print(f"Analyzing line: {line_number}")

        # Detect block start `{`
        if "{" in stripped_line:
            print(f"Line {line_number}: block start")
            inside_block = True
        if inside_block:
            block_lines.append(line)
            # Block end with `}`
            if "}" in stripped_line:
                print(f"Line {line_number}: block end")
                inside_block = False
                process_block(text_widget, block_lines, line_number - len(block_lines) + 1)
                block_lines = []
            continue
        
        # Analyze individual lines (outside block)
        process_line(text_widget, line, line_number)

        # Skip empty lines
        if not stripped_line:
            print(f"Line {line_number} is empty")
            continue

        # Remove tags only for the current line
        start_index = f"{line_number}.0"
        end_index = f"{line_number}.end"
        for tag in ["function", "conditional", "loop", "shape", "valid"]:
            text_widget.tag_remove(tag, start_index, end_index)
        # Analyze individual lines (outside block)
        print(f"Line {line_number}: analyzing outside block")
        process_line(text_widget, line, line_number)


def process_block(text_widget, block_lines, start_line):
    """
    Analyzes a complete block delimited by `{}`.
    """
    for tag in ["function", "conditional", "loop", "shape", "valid", "incorrect"]:
        text_widget.tag_remove(tag, "1.0", "end")
    print(f"Starting block analysis: line {start_line}")
    block_content = "\n".join(block_lines)

    # Lexical and syntactic analysis
    lexer = Lexer(block_content)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    is_valid, error = parser.parse()

    start_pos = f"{start_line}.0"
    end_pos = f"{start_line + len(block_lines) - 1}.end"

    if not is_valid:
        # Mark the entire block as incorrect
        print("Error in block")
        text_widget.tag_add("incorrect", start_pos, end_pos)
        # Display the error message for debugging or tooltip
        print(f"Error in block ({start_line}-{start_line + len(block_lines) - 1}): {error}")
        return

    # If the block is valid, apply tags
    print(f"Block is valid")
    token_positions = calculate_token_positions(block_content, tokens, start_line)
    apply_tags_with_lexer(text_widget, token_positions)
    print(f"Valid block detected ({start_line}-{start_line + len(block_lines) - 1}).")

def process_line(text_widget, line, line_number):
    """
    Analyzes a single line and applies tags.
    """
    start_index = f"{line_number}.0"
    end_index = f"{line_number}.end"

    # Remove old tags for this line
    for tag in ["function", "conditional", "loop", "shape", "keyword", "valid", "incorrect"]:
        text_widget.tag_remove(tag, start_index, end_index)

    if not line.strip():
        print(f"Line {line_number} is empty")
        return

    # Lexical and syntactic analysis
    lexer = Lexer(line)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    is_valid, error_message = parser.parse()

    print(f"Line {line_number} analyzed: {line}")
    print(f"Generated tokens: {tokens}")
    print(f"Line valid: {is_valid}")

    # If the line is invalid, mark it as incorrect
    if not is_valid:
        print(f"Line incorrect: {error_message}")
        text_widget.tag_add("incorrect", start_index, end_index)
        return

    # Apply tags for each token
    char_index = start_index
    for token_type, value in tokens:
        next_index = f"{char_index}+{len(value)}c"
        tag = get_tag_for_token_type(token_type)

        if tag:
            print(f"Applying tag {tag} on token '{value}' (line {line_number})")
            text_widget.tag_add(tag, char_index, next_index)

        char_index = next_index

def calculate_token_positions(content, tokens, start_line):
    """
    Calculates token positions in the content for multi-line blocks.
    """
    token_positions = []
    lines = content.splitlines()

    for line_index, line in enumerate(lines, start=start_line):
        current_col = 0  # Current position in the line

        for token_type, value in tokens:
            if value in line[current_col:]:
                start_col = line.index(value, current_col)
                end_col = start_col + len(value)

                start_pos = f"{line_index}.{start_col}"
                end_pos = f"{line_index}.{end_col}"
                token_positions.append((token_type, value, start_pos, end_pos))

                current_col = end_col

    return token_positions


def apply_tags_with_lexer(text_widget, token_positions):
    """
    Applies tags for each token.
    """
    for token_type, value, start_pos, end_pos in token_positions:
        tag = get_tag_for_token_type(token_type)
        if tag:
            text_widget.tag_add(tag, start_pos, end_pos)

def get_tag_for_token_type(token_type):
    """
    Returns the tag corresponding to a token type.
    """
    tags = {
        "KEYWORD": "keyword",
        "CONDITIONAL": "conditional",
        "LOOP": "loop",
        "FUNCTION": "function",
        "CONDITION": "shape",
        "SHAPE": "shape",
        "IDENTIFIER": "valid",
        "NUMBER": "valid",
        "UNKNOWN": "incorrect",
        "LPAREN": "valid",
        "RPAREN": "valid",
        "LBRACE": "valid",
        "RBRACE": "valid",
        "COMMA": "valid",
        "SEMICOLON": "valid",
        "VARIABLE": "valid",
        "NUMBER_OR_VARIABLE": "valid",
    }
    return tags.get(token_type)

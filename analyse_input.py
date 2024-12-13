from lexer import Lexer
from parser import Parser

def analyze_and_highlight(text_widget):
    for tag in ["keyword", "conditional", "shape", "valid", "incorrect"]:
        text_widget.tag_remove(tag, "1.0", "end")

    text = text_widget.get("1.0", "end-1c")
    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        start_index = f"{line_number}.0"
        end_index = f"{line_number}.end"

        if not line.strip():
            continue

        lexer = Lexer(line.strip())
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        is_valid, _ = parser.parse()

        if is_valid:
            apply_token_colors(text_widget, tokens, start_index)
        else:
            text_widget.tag_add("incorrect", start_index, end_index)



def apply_token_colors(text_widget, tokens, start_index):
    """
    Apply styles to tokens based on their type.
    """
    char_index = start_index
    for token_type, value in tokens:
        next_index = f"{char_index}+{len(value)}c"

        if token_type == "KEYWORD":
            text_widget.tag_add("keyword", char_index, next_index)  # Blue and bold
        elif token_type == "CONDITIONAL":
            text_widget.tag_add("conditional", char_index, next_index)  # Green
        elif token_type == "SHAPE":
            text_widget.tag_add("shape", char_index, next_index)  # Violet
        elif token_type in ["NUMBER", "LPAREN", "RPAREN", "COMMA", "COLON"]:
            text_widget.tag_add("valid", char_index, next_index)  # Black
        else:
            text_widget.tag_add("incorrect", char_index, next_index)  # Red

        char_index = next_index

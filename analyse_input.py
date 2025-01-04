from lexer import Lexer
from parser import Parser

def analyze_and_highlight(text_widget):
    # Retirer tous les tags précédents
    for tag in ["function", "conditional", "loop", "shape", "valid", "incorrect"]:
        text_widget.tag_remove(tag, "1.0", "end")

    # Récupérer le texte de la zone
    text = text_widget.get("1.0", "end-1c")
    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        start_index = f"{line_number}.0"
        end_index = f"{line_number}.end"

        # Analyse lexicale et syntaxique
        lexer = Lexer(line)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        is_valid, error_message = parser.parse()

        # Appliquer les styles pour chaque token
        char_index = start_index
        for token_type, value in tokens:
            next_index = f"{char_index}+{len(value)}c"
            if token_type == "KEYWORD":
                text_widget.tag_add("function", char_index, next_index)
            elif token_type == "CONDITIONAL":
                text_widget.tag_add("conditional", char_index, next_index)
            elif token_type == "LOOP":
                text_widget.tag_add("loop", char_index, next_index)
            elif token_type == "SHAPE":
                text_widget.tag_add("shape", char_index, next_index)
            elif is_valid:
                text_widget.tag_add("valid", char_index, next_index)
            else:
                text_widget.tag_add("incorrect", char_index, next_index)
            char_index = next_index

        # Si la ligne entière est incorrecte, taguer toute la ligne
        if not is_valid:
            text_widget.tag_add("incorrect", start_index, end_index)

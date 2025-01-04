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

        # Si la ligne est incorrecte, marquer toute la ligne
        if not is_valid:
            text_widget.tag_add("incorrect", start_index, end_index)
            continue

        # Appliquer les styles pour chaque token
        char_index = start_index
        command_name = tokens[0][1] if tokens and tokens[0][0] == "KEYWORD" else None
        for i, (token_type, value) in enumerate(tokens):
            next_index = f"{char_index}+{len(value)}c"
            if token_type == "KEYWORD":
                text_widget.tag_add("function", char_index, next_index)
            elif token_type == "CONDITIONAL":
                text_widget.tag_add("conditional", char_index, next_index)
            elif token_type == "LOOP":
                text_widget.tag_add("loop", char_index, next_index)
            elif token_type == "SHAPE":
                text_widget.tag_add("shape", char_index, next_index)
            elif token_type == "NUMBER":
                # Vérification des contraintes pour les valeurs numériques
                is_valid, error_message = parser._check_constraints(
                    (token_type, value), command_name, i - 1
                )
                if not is_valid:
                    text_widget.tag_add("incorrect", char_index, next_index)
                else:
                    text_widget.tag_add("valid", char_index, next_index)
            else:
                text_widget.tag_add("valid", char_index, next_index)
            char_index = next_index

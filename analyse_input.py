from lexer import Lexer
from parser import Parser

def process_and_color_line_by_line_with_blocks(text_widget):
    """
    Analyse le contenu ligne par ligne et traite les blocs complets.
    """
    # Récupérer le contenu du widget texte
    content = text_widget.get("1.0", "end-1c")
    lines = content.splitlines()
    inside_block = False
    block_lines = []

    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()

        # Détection de début de bloc `{`
        if "{" in stripped_line:
            inside_block = True
        if inside_block:
            block_lines.append(line)
            # Fin de bloc avec `}`
            if "}" in stripped_line:
                inside_block = False
                process_block(text_widget, block_lines, line_number - len(block_lines) + 1)
                block_lines = []
            continue

        #Supprimer uniquement les tags sur la ligne actuelle
        start_index = f"{line_number}.0"
        end_index = f"{line_number}.end"
        for tag in ["function", "conditional", "loop", "shape", "valid", "incorrect"]:
            text_widget.tag_remove(tag, start_index, end_index)
        # Analyse des lignes seules (hors bloc)
        process_line(text_widget, line, line_number)
    
   

def process_block(text_widget, block_lines, start_line):
    """
    Analyse un bloc complet délimité par `{}`.
    """
    for tag in ["function", "conditional", "loop", "shape", "valid", "incorrect"]:
        text_widget.tag_remove(tag, "1.0", "end")
    block_content = "\n".join(block_lines)

    # Analyse lexicale et syntaxique
    lexer = Lexer(block_content)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    is_valid, error = parser.parse()

    start_pos = f"{start_line}.0"
    end_pos = f"{start_line + len(block_lines) - 1}.end"

    if not is_valid:
        # Marquer tout le bloc comme incorrect
        text_widget.tag_add("incorrect", start_pos, end_pos)
        # Afficher le message d'erreur pour débogage ou tooltip
        print(f"Erreur dans le bloc ({start_line}-{start_line + len(block_lines) - 1}): {error}")
        return

    # Si le bloc est valide, appliquer les tags
    token_positions = calculate_token_positions(block_content, tokens, start_line)
    apply_tags_with_lexer(text_widget, token_positions)
    print(f"Bloc valide détecté ({start_line}-{start_line + len(block_lines) - 1}).")

    

def process_line(text_widget, line, line_number):
    """
    Analyse une ligne seule et applique les tags.
    """
    for tag in ["function", "conditional", "loop", "shape", "valid", "incorrect"]:
        text_widget.tag_remove(tag, "1.0", "end")

    # Récupérer le texte de la zone
    text = text_widget.get("1.0", "end-1c")
    lines = text.splitlines()
    
    # Ignorer les lignes vides
    if not line.strip():
        return

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
                text_widget.tag_add("keyword", char_index, next_index)
            elif token_type == "CONDITIONAL":
                text_widget.tag_add("conditional", char_index, next_index)
            elif token_type == "LOOP":
                text_widget.tag_add("loop", char_index, next_index)
            elif token_type == "SHAPE":
                text_widget.tag_add("shape", char_index, next_index)
            elif token_type == "FUNCTION":
                text_widget.tag_add("function", char_index, next_index)
            elif is_valid:
                text_widget.tag_add("valid", char_index, next_index)
            else:
                text_widget.tag_add("incorrect", char_index, next_index)
            char_index = next_index

        # Si la ligne entière est incorrecte, taguer toute la ligne
        if not is_valid:
            text_widget.tag_add("incorrect", start_index, end_index)

def calculate_token_positions(content, tokens, start_line):
    """
    Calcule les positions des tokens dans le contenu.
    """
    token_positions = []
    lines = content.splitlines()

    for line_index, line in enumerate(lines, start=start_line):
        current_col = 0  # Position dans la ligne

        for token_type, value in tokens:
            if value in line[current_col:]:
                start_col = line.index(value, current_col)
                end_col = start_col + len(value)

                start_pos = f"{line_index}.{start_col}"
                end_pos = f"{line_index}.{end_col}"
                token_positions.append((token_type, value, start_pos, end_pos))

                # Mettre à jour current_col pour éviter des doublons
                current_col = end_col

    return token_positions

def apply_tags_with_lexer(text_widget, token_positions):
    """
    Applique les tags pour chaque token.
    """
    for token_type, value, start_pos, end_pos in token_positions:
        tag = get_tag_for_token_type(token_type)
        if tag:
            text_widget.tag_add(tag, start_pos, end_pos)

def get_tag_for_token_type(token_type):
    """
    Renvoie le tag correspondant au type de token.
    """
    tags = {
        "KEYWORD": "keyword",
        "CONDITIONAL": "conditional",
        "LOOP": "loop",
        "FUNCTION": "function",
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
    }
    return tags.get(token_type)

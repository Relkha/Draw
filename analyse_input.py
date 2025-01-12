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
    block_start_line = 0

    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        print(f"Anlyse de la ligne : {line_number}")

        # Détection de début de bloc `{`
        if "{" in stripped_line:
            print(f"ligne {line_number} : debut de bloc")
            inside_block = True
        if inside_block:
            block_lines.append(line)
            # Fin de bloc avec `}`
            if "}" in stripped_line:
                print(f"ligne{line_number} : fin de bloc")
                inside_block = False
                process_block(text_widget, block_lines, line_number - len(block_lines) + 1)
                block_lines = []
            continue
        
        # Analyse des lignes seules (hors bloc)
        process_line(text_widget, line, line_number)

        # Si la ligne est vide, continuez à analyser les suivantes
        if not stripped_line:
            print(f"ligne {line_number} vide")
            continue

        #Supprimer uniquement les tags sur la ligne actuelle
        start_index = f"{line_number}.0"
        end_index = f"{line_number}.end"
        for tag in ["function", "conditional", "loop", "shape", "valid"]:
            text_widget.tag_remove(tag, start_index, end_index)
        # Analyse des lignes seules (hors bloc)
        print(f"lignbe{line_number} : analyse ligne hors bloc")
        process_line(text_widget, line, line_number)

    
   


def process_block(text_widget, block_lines, start_line):
    """
    Analyse un bloc complet délimité par `{}`.
    """
    for tag in ["function", "conditional", "loop", "shape", "valid", "incorrect"]:
        text_widget.tag_remove(tag, "1.0", "end")
    print(f"debut analyse bloc : ligne {start_line}")
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
        print("erreur dans le bloc")
        text_widget.tag_add("incorrect", start_pos, end_pos)
        # Afficher le message d'erreur pour débogage ou tooltip
        print(f"Erreur dans le bloc ({start_line}-{start_line + len(block_lines) - 1}): {error}")
        return

    # Si le bloc est valide, appliquer les tags
    print(f"bloc valide")
    token_positions = calculate_token_positions(block_content, tokens, start_line)
    apply_tags_with_lexer(text_widget, token_positions)
    print(f"Bloc valide détecté ({start_line}-{start_line + len(block_lines) - 1}).")

def process_line(text_widget, line, line_number):
    """
    Analyse une seule ligne et applique les tags.
    """
    start_index = f"{line_number}.0"
    end_index = f"{line_number}.end"

    # Supprimer les anciens tags pour cette ligne
    for tag in ["function", "conditional", "loop", "shape", "keyword", "valid", "incorrect"]:
        text_widget.tag_remove(tag, start_index, end_index)

    if not line.strip():
        print(f"Ligne {line_number} vide")
        return

    # Analyse lexicale et syntaxique
    lexer = Lexer(line)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    is_valid, error_message = parser.parse()

    print(f"Ligne {line_number} analysée : {line}")
    print(f"Tokens générés : {tokens}")
    print(f"Ligne valide : {is_valid}")

    # Si la ligne est incorrecte, marquer la ligne comme incorrecte
    if not is_valid:
        print(f"Ligne incorrecte : {error_message}")
        text_widget.tag_add("incorrect", start_index, end_index)
        return

    # Appliquer les tags pour chaque token
    char_index = start_index
    for token_type, value in tokens:
        next_index = f"{char_index}+{len(value)}c"
        tag = get_tag_for_token_type(token_type)

        if tag:
            print(f"Appliquer tag {tag} sur le token '{value}' (ligne {line_number})")
            text_widget.tag_add(tag, char_index, next_index)

        char_index = next_index

def calculate_token_positions(content, tokens, start_line):
    """
    Calcule les positions des tokens dans le contenu pour des blocs multi-lignes.
    """
    token_positions = []
    lines = content.splitlines()

    for line_index, line in enumerate(lines, start=start_line):
        current_col = 0  # Position actuelle dans la ligne

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
    Applique les tags pour chaque token.
    """
    for token_type, value, start_pos, end_pos in token_positions:
        tag = get_tag_for_token_type(token_type)
        if tag:
            text_widget.tag_add(tag, start_pos, end_pos)

def get_tag_for_token_type(token_type):
    """
    Retourne le tag correspondant à un type de token.
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

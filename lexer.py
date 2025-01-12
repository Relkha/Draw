import re
import json

# Charger les commandes depuis le JSON
with open("keywords.json", "r") as f:
    keywords_data = json.load(f)
commands_ = "|".join(keywords_data["commands"].keys())  # Mots-clés des commandes
conditionals_ = "|".join(keywords_data["conditionals"].keys())  # Mots-clés des conditionnels
shapes_ = "|".join(keywords_data["shapes"])  # Mots-clés des formes
loops_ = "|".join(keywords_data["loops"].keys())  # Mots-clés des boucles
block_content_ = "|".join(keywords_data["block_content"]["type"])  # Types dans block_content
function_ = "|".join(keywords_data["function"].keys()) #pour les fonctions

# Récupérer les types dans block_content et leurs sous-types
block_content_types = keywords_data["block_content"]["type"]
block_content_keywords = {
    key: "|".join(keywords_data[key].keys()) if key in keywords_data else ""
    for key in block_content_types
}

# Définir les types de tokens pour la nouvelle syntaxe
TOKEN_TYPES = [
    ('EQUALS', r'='),  # Opérateur égal
    ('LOOP', rf'\b({loops_})\b'),  # Mots-clés des boucles
    ('FUNCTION', rf'\b({function_})\b'),  # Mots-clés des fonctions
    ('KEYWORD', rf'\b({commands_})\b'),  # Mots-clés des commandes
    ('CONDITIONAL', rf'\b({conditionals_})\b'),  # Mots-clés conditionnels
    ('CONDITION', r'[a-zA-Z]\s*(<|>|==)\s*\d+'),  # Variable suivie d'un comparateur et d'un nombre
    ('SHAPE', rf'\b({shapes_})\b'),  # Formes valides
    ('VARIABLE', r'[a-z]'),  # Variables définies par des lettres minuscules
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiants
    ('NUMBER', r'\d+'),  # Nombres
    ('LPAREN', r'\('),  # Parenthèse gauche
    ('RPAREN', r'\)'),  # Parenthèse droite
    ('LBRACE', r'\{'),  # Accolade gauche
    ('RBRACE', r'\}'),  # Accolade droite
    ('COMMA', r','),  # Virgule
    ('COLON', r':'),  # Deux-points
    ('SEMICOLON', r';'),  # Point-virgule
    ('WHITESPACE', r'\s+'),  # Espaces blancs
    ('UNKNOWN', r'.')  # Caractères non reconnus
]

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.position = 0

    def _match(self, expected_type):
        current_token = self._current_token()
        if not current_token:
            return False
        token_type, value = current_token
        if expected_type == "CONDITION":
            # Une condition peut être une comparaison ou une forme
            return token_type in ["CONDITION", "SHAPE"]
        if expected_type == "NUMBER_OR_VARIABLE":
            return token_type in ["NUMBER", "VARIABLE"]
        return token_type == expected_type

    
    def _get_token(self):
        if self.position >= len(self.code):
            return None  # Fin du code

        temp_accumulator = ""
        for token_type, regex in TOKEN_TYPES:
            match = re.match(regex, self.code[self.position:])
            if match:
                value = match.group(0)

                if token_type == "CONDITION":
                    # Vérifier si le dernier token ajouté est déjà identique
                    if self.tokens and self.tokens[-1] == (token_type, value):
                        self.position += len(value)
                        return None 
                elif token_type == "SHAPE":
                    # Vérifier le contexte
                    if self.tokens and self.tokens[-1][0] == "LPAREN":
                        token_type = "CONDITION"  # Traiter comme une condition
                    else:
                        token_type = "SHAPE" 
                
                # Accumuler les caractères pour VARIABLE ou IDENTIFIER
                elif token_type in ["IDENTIFIER", "VARIABLE"]:
                    temp_accumulator += value
                    self.position += len(value)
                    continue

                # Traiter l'accumulateur lorsqu'un autre token est rencontré
                if temp_accumulator:
                    # Si une seule lettre minuscule, c'est une VARIABLE
                    if len(temp_accumulator) == 1 and temp_accumulator.islower():
                        self.tokens.append(("VARIABLE", temp_accumulator))
                    else:
                        self.tokens.append(("IDENTIFIER", temp_accumulator))
                    temp_accumulator = ""
                # Ajouter le token si ce n'est pas un espace
                if token_type == 'IDENTIFIER':
                    if value in commands_.split('|') or \
                       value in loops_.split('|') or \
                       value in conditionals_.split('|') or \
                       value in function_.split('|') or \
                       any(value in block_content_keywords[key].split('|') for key in block_content_keywords):
                        token_type = 'KEYWORD'  # Reclasser les mots-clés valides
                    else:
                        token_type = 'IDENTIFIER'  # Identifiant valide

                if token_type == 'NUMBER':
                    if not re.match(r'\d+', value):
                        token_type = 'UNKNOWN'
                if token_type != 'WHITESPACE':
                    self.tokens.append((token_type, value))

                self.position += len(value)
                return value

        # Si aucun match trouvé, lever une erreur
        if not temp_accumulator:
            char = self.code[self.position]
            print(f"Caractère invalide détecté : {char} à la position {self.position}")
            self.tokens.append(("UNKNOWN", char))
            self.position += 1  # Avancer d'un caractère
            return char
         # Traiter l'accumulateur à la fin
        if temp_accumulator:
            if len(temp_accumulator) == 1 and temp_accumulator.islower():
                self.tokens.append(("VARIABLE", temp_accumulator))
            else:
                self.tokens.append(("IDENTIFIER", temp_accumulator))
    

    def tokenize(self):
        while self.position < len(self.code):
            self._get_token()
        return self.tokens
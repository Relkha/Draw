import re
import json

# Charger les commandes depuis le JSON
with open("keywords.json", "r") as f:
    keywords_data = json.load(f)
commands_ = "|".join(keywords_data["commands"].keys())  # Mots-clés des commandes
conditionals_ = "|".join(keywords_data["conditionals"].keys())  # Mots-clés des conditionnels
shapes_ = "|".join(keywords_data["shapes"])  # Mots-clés des formes

# Définir les types de tokens pour la nouvelle syntaxe
TOKEN_TYPES = [
    ('KEYWORD', rf'\b({commands_})\b'),  # Mots-clés des commandes
    ('CONDITIONAL', rf'\b({conditionals_})\b'),  # Mots-clés conditionnels
    ('SHAPE', rf'\b({shapes_})\b'),  # Formes valides
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiants (ex. C)
    ('NUMBER', r'\d+'),  # Nombres (ex. 150, 100)
    ('LPAREN', r'\('),  # Parenthèse gauche
    ('RPAREN', r'\)'),  # Parenthèse droite
    ('COMMA', r','),  # Virgule pour séparer les coordonnées
    ('COLON', r':'),  # Deux-points
    ('WHITESPACE', r'\s+'),  # Espaces blancs
    ('UNKNOWN', r'.')  # Tout autre caractère non reconnu
]

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.position = 0

    def _get_token(self):
        if self.position >= len(self.code):
            return None  # Fin du code

        for token_type, regex in TOKEN_TYPES:
            match = re.match(regex, self.code[self.position:])
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':  # Ignorer les espaces
                    self.tokens.append((token_type, value))
                self.position += len(value)
                return value
        raise SyntaxError(f"Invalid character at position {self.position}")

    def tokenize(self):
        while self.position < len(self.code):
            self._get_token()
        return self.tokens

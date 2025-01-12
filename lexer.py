# A Python lexer for tokenizing Draw++ commands from a JSON-based keyword configuration
import re
import json

# Load command keywords from a JSON file
with open("keywords.json", "r") as f:
    keywords_data = json.load(f)
commands_ = "|".join(keywords_data["commands"].keys())
conditionals_ = "|".join(keywords_data["conditionals"].keys())
shapes_ = "|".join(keywords_data["shapes"])
loops_ = "|".join(keywords_data["loops"].keys())
block_content_ = "|".join(keywords_data["block_content"]["type"])
function_ = "|".join(keywords_data["function"].keys())

# Extract block content types and subtypes
block_content_types = keywords_data["block_content"]["type"]
block_content_keywords = {
    key: "|".join(keywords_data[key].keys()) if key in keywords_data else ""
    for key in block_content_types
}

# Define token types for the Draw++ syntax
TOKEN_TYPES = [
    ('EQUALS', r'='),
    ('LOOP', rf'\b({loops_})\b'),
    ('FUNCTION', rf'\b({function_})\b'),
    ('KEYWORD', rf'\b({commands_})\b'),
    ('CONDITIONAL', rf'\b({conditionals_})\b'),
    ('CONDITION', r'[a-zA-Z]\s*(<|>|==)\s*\d+'),
    ('SHAPE', rf'\b({shapes_})\b'),
    ('VARIABLE', r'[a-z]'),
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('NUMBER', r'\d+'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COMMA', r','),
    ('COLON', r':'),
    ('SEMICOLON', r';'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.')
]

class Lexer:
    """
    Lexer for tokenizing code into a stream of tokens based on predefined patterns.
    """
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.position = 0

    def _match(self, expected_type):
        """
        Match a token type with the current token in the stream.
        """
        current_token = self._current_token()
        if not current_token:
            return False
        token_type, value = current_token
        if expected_type == "CONDITION":
            return token_type in ["CONDITION", "SHAPE"]
        if expected_type == "NUMBER_OR_VARIABLE":
            return token_type in ["NUMBER", "VARIABLE"]
        return token_type == expected_type

    def _get_token(self):
        """
        Extract the next token from the input code based on the defined patterns.
        """
        if self.position >= len(self.code):
            return None

        temp_accumulator = ""
        for token_type, regex in TOKEN_TYPES:
            match = re.match(regex, self.code[self.position:])
            if match:
                value = match.group(0)

                if token_type == "CONDITION":
                    if self.tokens and self.tokens[-1] == (token_type, value):
                        self.position += len(value)
                        return None
                elif token_type == "SHAPE":
                    if self.tokens and self.tokens[-1][0] == "LPAREN":
                        token_type = "CONDITION"
                    else:
                        token_type = "SHAPE"

                elif token_type in ["IDENTIFIER", "VARIABLE"]:
                    temp_accumulator += value
                    self.position += len(value)
                    continue

                if temp_accumulator:
                    if len(temp_accumulator) == 1 and temp_accumulator.islower():
                        self.tokens.append(("VARIABLE", temp_accumulator))
                    else:
                        self.tokens.append(("IDENTIFIER", temp_accumulator))
                    temp_accumulator = ""

                if token_type == 'IDENTIFIER':
                    if value in commands_.split('|') or \
                       value in loops_.split('|') or \
                       value in conditionals_.split('|') or \
                       value in function_.split('|') or \
                       any(value in block_content_keywords[key].split('|') for key in block_content_keywords):
                        token_type = 'KEYWORD'
                    else:
                        token_type = 'IDENTIFIER'

                if token_type == 'NUMBER' and not re.match(r'\d+', value):
                    token_type = 'UNKNOWN'
                if token_type != 'WHITESPACE':
                    self.tokens.append((token_type, value))

                self.position += len(value)
                return value

        if not temp_accumulator:
            char = self.code[self.position]
            print(f"Invalid character detected: {char} at position {self.position}")
            self.tokens.append(("UNKNOWN", char))
            self.position += 1
            return char

        if temp_accumulator:
            if len(temp_accumulator) == 1 and temp_accumulator.islower():
                self.tokens.append(("VARIABLE", temp_accumulator))
            else:
                self.tokens.append(("IDENTIFIER", temp_accumulator))

    def tokenize(self):
        """
        Tokenizes the entire code into a list of tokens.
        """
        while self.position < len(self.code):
            self._get_token()
        return self.tokens

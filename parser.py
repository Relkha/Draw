import json

# Charger keywords.json
with open("keywords.json") as f:
    keywords_data = json.load(f)

commands = keywords_data["commands"]  # Commandes standards
conditionals = keywords_data["conditionals"]  # Blocs conditionnels
shapes = keywords_data["shapes"]  # Formes valides


import json

# Charger keywords.json
with open("keywords.json") as f:
    keywords_data = json.load(f)

commands = keywords_data["commands"]  # Commandes standards
conditionals = keywords_data["conditionals"]  # Blocs conditionnels
shapes = keywords_data["shapes"]  # Formes valides


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def _current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _advance(self):
        if self.position < len(self.tokens):
            self.position += 1

    def parse(self):
        """
        Main parsing method for both simple commands and conditionals.
        """
        current = self._current_token()
        if not current:
            return False, "No tokens to parse"

        if current[0] == "KEYWORD":
            return self._parse_simple_command()
        elif current[0] == "CONDITIONAL":
            return self._parse_conditional(current[1])
        else:
            return False, f"Unexpected token: {current[0]}"

    def _parse_simple_command(self):
        # Validate a simple command (e.g., create_cursor).
        command = self._current_token()
        if command[0] != "KEYWORD":
            return False, "Expected a command keyword"

        self._advance()
        if not self._current_token() or self._current_token()[0] != "IDENTIFIER":
            return False, "Expected an identifier"

        self._advance()
        if not self._current_token() or self._current_token()[0] != "LPAREN":
            return False, "Expected '('"

        self._advance()
        while self._current_token() and self._current_token()[0] != "RPAREN":
            if self._current_token()[0] not in ["NUMBER", "COMMA"]:
                return False, "Expected numbers or ',' inside parentheses"
            self._advance()

        if not self._current_token() or self._current_token()[0] != "RPAREN":
            return False, "Expected ')'"

        self._advance()
        return True, None

    def _parse_conditional(self, keyword):
        # Validate a conditional block (e.g., if, else).
        self._advance()
        if keyword == "if":
            if not self._current_token() or self._current_token()[0] != "LPAREN":
                return False, "Expected '(' after 'if'"
            self._advance()
            if not self._current_token() or self._current_token()[0] != "SHAPE":
                return False, "Expected a shape in 'if' condition"
            self._advance()
            if not self._current_token() or self._current_token()[0] != "RPAREN":
                return False, "Expected ')'"
            self._advance()

        if not self._current_token() or self._current_token()[0] != "COLON":
            return False, f"Expected ':' after '{keyword}'"
        self._advance()

        while self._current_token() and self._current_token()[0] in ["KEYWORD", "IDENTIFIER"]:
            success, error_message = self.parse()
            if not success:
                return False, error_message

        return True, None

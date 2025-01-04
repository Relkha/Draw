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
        """Retourne le token actuel."""
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _advance(self):
        """Avance à la prochaine position des tokens."""
        if self.position < len(self.tokens):
            self.position += 1

    def _match(self, expected_type):
        """Vérifie si le token courant correspond au type attendu."""
        token = self._current_token()
        if token and token[0] == expected_type:
            self._advance()
            return True
        return False

    def parse(self):
        """
        Méthode principale pour analyser les commandes.
        """
        current = self._current_token()
        if not current:
            return False, "No tokens to parse"

        if current[0] == "KEYWORD":
            return self._parse_simple_command()
        elif current[0] == "CONDITIONAL":
            return self._parse_conditional(current[1])
        elif current[0] == "LOOP":
            return self._parse_loop()
        else:
            return False, f"Unexpected token: {current[0]}"

    def _parse_simple_command(self):
        """
        Valide une commande simple en se basant sur keywords.json.
        """
        command = self._current_token()
        if not command or command[0] != "KEYWORD":
            return False, "Expected a command keyword"

        command_name = command[1]
        if command_name not in commands:
            return False, f"Unknown command: {command_name}"

        expected_args = commands[command_name]["args"]  # Arguments attendus depuis keywords.json
        self._advance()

        for expected_type in expected_args:
            # Ignorer les espaces (WHITESPACE) s'ils existent
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()
            
            if not self._match(expected_type):
                return False, f"Expected {expected_type} after {command_name}"

        return True, None

    def _parse_conditional(self, keyword):
        """
        Valide une instruction conditionnelle (if / else).
        """
        if keyword not in conditionals:
            return False, f"Unknown conditional: {keyword}"

        expected_args = conditionals[keyword]["args"]
        self._advance()

        for expected_type in expected_args:
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()
            
            if not self._match(expected_type):
                return False, f"Expected {expected_type} in conditional block"

        return True, None

    def _parse_loop(self):
        """
        Valide une boucle de type `repeat` en se basant sur keywords.json.
        """
        loop_keyword = self._current_token()
        if not loop_keyword or loop_keyword[1] != "repeat":
            return False, "Expected 'repeat' keyword"

        # Récupération des arguments attendus depuis keywords.json
        expected_args = keywords_data["loops"]["repeat"]["args"]
        self._advance()  # Avancer après le mot-clé 'repeat'

        for expected_type in expected_args:
            # Ignorer les espaces (WHITESPACE)
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            # Vérifier si le token correspond au type attendu
            if not self._match(expected_type):
                return False, f"Expected {expected_type} in loop declaration"

        return True, None
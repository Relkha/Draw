import json

# Charger keywords.json
with open("keywords.json") as f:
    keywords_data = json.load(f)

commands = keywords_data["commands"]  # Commandes standards
conditionals = keywords_data["conditionals"]  # Blocs conditionnels
shapes = keywords_data["shapes"]  # Formes valides
loops = keywords_data["loops"] #boucle

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
            return self._parse_loop(current[1])
        else:
            return False, f"Unexpected token: {current[0]}"

    def _check_constraints(self, token, command_name, arg_index):
        """
        Vérifie les contraintes définies dans keywords.json pour une commande spécifique.
        """
        # Récupération des contraintes pour la commande actuelle
        constraints = commands.get(command_name, {}).get("constraints", {})
        arg_constraints = constraints.get("args", {})

        if token[0] == "NUMBER":
            try:
                value = int(token[1])  # Convertir la valeur en entier
            except ValueError:
                return False, f"Invalid number format: {token[1]}"

            # Vérifier les limites des nombres si elles existent
            if "NUMBER" in arg_constraints:
                min_val = arg_constraints["NUMBER"].get("min", float("-inf"))
                max_val = arg_constraints["NUMBER"].get("max", float("inf"))
                if not (min_val <= value <= max_val):
                    return False, (
                        f"Value {value} for argument {arg_index + 1} "
                        f"is out of range [{min_val}, {max_val}]"
                    )

        return True, None

    def _parse_simple_command(self):
        """
        Validates a simple command based on keywords.json.
        """
        command = self._current_token()
        if not command or command[0] != "KEYWORD":
            return False, "Expected a command keyword"

        command_name = command[1]
        if command_name not in commands:
            return False, f"Unknown command: {command_name}"

        expected_args = commands[command_name]["args"]  # Expected arguments from keywords.json
        self._advance()

        for i, expected_type in enumerate(expected_args):
            # Ignore whitespace tokens if they exist
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            current_token = self._current_token()
            if not current_token or not self._match(expected_type):
                return False, f"Expected {expected_type} after {command_name}"

            is_valid, error_message = self._check_constraints(current_token, command_name, i)
            if not is_valid:
                return False, error_message

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
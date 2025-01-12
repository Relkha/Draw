import json

# Charger keywords.json
with open("keywords.json") as f:
    keywords_data = json.load(f)

commands = keywords_data["commands"]
loops = keywords_data["loops"]
conditionals = keywords_data["conditionals"]
functions = keywords_data["function"]
shapes = keywords_data["shapes"]  # Formes valides


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.last_conditional = None

    def _current_token(self):
        """Retourne le token actuel."""
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _advance(self):
        """Avance à la prochaine position des tokens."""
        if self.position < len(self.tokens):
            self.position += 1

    def _match(self, token_type):
        current = self._current_token()
        # Vérifier si le token courant est valide
        if current:
            current_type, current_value = current

            # Gestion spécifique pour NUMBER_OR_VARIABLE
            if token_type == "CONDITION":
                if current_type in ["CONDITION", "SHAPE"]:
                    print(f"Match trouvé (CONDITION ou SHAPE) : {current}")
                    self._advance()
                    print(f"Après _advance : token actuel = {self._current_token()}")
                    return True
            if token_type == "NUMBER_OR_VARIABLE":
                if current_type in ["NUMBER", "VARIABLE"]:
                    print(f"Match trouvé (NUMBER_OR_VARIABLE) : {current}")
                    self._advance()
                    print(f"Après _advance : token actuel = {self._current_token()}")
                    return True
            if current_type == token_type:
                print(f"Match trouvé : {current}")
                self._advance()
                print(f"Après _advance : token actuel = {self._current_token()}")
                return True
        print(f"Pas de match : {current}")
        return False



    def parse(self):
        """
        Méthode principale pour analyser les commandes.
        """
        while self._current_token():
            current = self._current_token()
            if current[0] == "KEYWORD":
                is_valid, error = self._parse_simple_command()
                if not is_valid:
                    return False, error
            elif current[0] == "CONDITIONAL":
                is_valid, error = self._parse_conditional(current[1])
                if not is_valid:
                    return False, error
            elif current[0] == "LOOP":
                is_valid, error = self._parse_loop(current[1])
                if not is_valid:
                    return False, error
            elif current[0] == "FUNCTION":
                is_valid, error = self._parse_function(current[1])
                if not is_valid:
                    return False, error
            elif current[0] == "RBRACE":
                # Fin d'un bloc de boucle ou de conditionnel
                return True, None
            else:
                return False, f"Unexpected token: {current[0]}"
        return True, None


    def _parse_function(self, keyword):
        """
        Valide une déclaration de fonction.
        """
        if keyword not in functions:
            return False, f"Unknown function keyword: {keyword}"

        expected_args = functions[keyword]["args"]
        self._advance()

        for expected_type in expected_args:
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            if expected_type == "block_content":
                while self._current_token():
                    current_token = self._current_token()

                    if current_token[0] == "RBRACE":
                        self._advance()
                        return True, None

                    if current_token[0] == "KEYWORD":
                        is_valid, error = self._parse_simple_command()
                    elif current_token[0] == "CONDITIONAL":
                        is_valid, error = self._parse_conditional(current_token[1])
                    elif current_token[0] == "LOOP":
                        is_valid, error = self._parse_loop(current_token[1])
                    else:
                        return False, f"Unexpected token in function block: {current_token}"

                    if not is_valid:
                        return False, error

            elif not self._match(expected_type):
                return False, f"Expected {expected_type} in function declaration"

        return True, None

    
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
        Valide une commande simple basée sur keywords.json.
        """
        command = self._current_token()
        print(f"Analyse de la commande : {command}")
        if not command or command[0] != "KEYWORD":
            return False, "Expected a command keyword"

        command_name = command[1]
        if command_name not in commands:
            return False, f"Unknown command: {command_name}"

        expected_args = commands[command_name]["args"]
        self._advance()

        for i, expected_type in enumerate(expected_args):
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            current_token = self._current_token()
            # Stopper l'analyse si on atteint RBRACE
            if current_token and current_token[0] == "RBRACE":
                print("Fin prématurée de la commande : '}' trouvé.")
                return True, None
            if not current_token or not self._match(expected_type):
                return False, f"Expected {expected_type} after {command_name}"

            is_valid, error_message = self._check_constraints(current_token, command_name, i)
            if not is_valid:
                return False, error_message

        # Ignorer un point-virgule optionnel
        if self._current_token() and self._current_token()[0] == "SEMICOLON":
            self._advance()

        return True, None


    def _parse_conditional(self, keyword):
        """
        Valide une instruction conditionnelle (if / else).
        """
        print(f"Début de l'analyse du conditionnel : {keyword}")
        
    
        if keyword not in conditionals:
            print(f"Erreur : conditionnel inconnu : {keyword}")
            return False, f"Unknown conditional: {keyword}"

        self.last_conditional = keyword
        self._advance()  # Avancer après le mot-clé conditionnel

        expected_args = conditionals[keyword]["args"]

        for expected_type in expected_args:
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            current_token = self._current_token()

            # Gestion des CONDITIONS (peuvent inclure des SHAPE)
            if expected_type == "CONDITION":
                if current_token and current_token[0] in ["CONDITION", "SHAPE"]:
                    print(f"Condition valide trouvée : {current_token}")
                    self._advance()
                    continue
                else:
                    return False, f"Expected CONDITION or SHAPE, but found {current_token}"
        
            # Bloc de contenu
            elif expected_type == "block_content":
                while self._current_token():
                    current_token = self._current_token()

                    if current_token[0] == "RBRACE":
                        print("Fin du bloc détectée avec 'RBRACE'.")
                        self._advance()
                        return True, None

                    if current_token[0] == "KEYWORD":
                        is_valid, error = self._parse_simple_command()
                    elif current_token[0] == "CONDITIONAL":
                        is_valid, error = self._parse_conditional(current_token[1])
                    elif current_token[0] == "LOOP":
                        is_valid, error = self._parse_loop(current_token[1])
                    else:
                        return False, f"Unexpected token in block_content: {current_token}"

                    if not is_valid:
                        return False, error

            # Validation des autres types attendus
            elif not self._match(expected_type):
                return False, f"Expected {expected_type}, but found {current_token}"

        return True, None



    def _parse_loop(self, keyword):
        """
        Analyse une boucle comme 'repeat', en suivant les définitions dans keywords.json.
        """
        print(f"Début de l'analyse de la boucle : {keyword}")
        if keyword not in loops:
            print(f"Erreur : boucle inconnue : {keyword}")
            return False, f"Unknown loop: {keyword}"

        # Avancer après le mot-clé de boucle
        self._advance()
        print(f"Après avoir avancé : token actuel = {self._current_token()}")

        # Valider les arguments de la boucle
        expected_args = loops[keyword]["args"]
        for expected_type in expected_args:
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            print(f"Validation de l'argument attendu : {expected_type}")
            if expected_type in "block_content":
                while self._current_token():
                    current_token = self._current_token()

                    if current_token[0] == "RBRACE":
                        print("Fin du bloc détectée avec 'RBRACE'.")
                        self._advance()
                        return True, None

                    if current_token[0] == "KEYWORD":
                        is_valid, error = self._parse_simple_command()
                    elif current_token[0] == "CONDITIONAL":
                        is_valid, error = self._parse_conditional(current_token[1])
                    elif current_token[0] == "LOOP":
                        is_valid, error = self._parse_loop(current_token[1])
                    else:
                        return False, f"Unexpected token in loop block: {current_token}"

                    if not is_valid:
                        return False, error

            elif not self._match(expected_type):
                return False, f"Expected {expected_type} in {keyword} declaration"

        # Validation finale pour RBRACE
        current_token = self._current_token()
        if current_token and current_token[0] == "RBRACE":
            print(f"Validation finale réussie pour 'RBRACE' : {current_token}")
            return True, None

        print("Erreur : accolade fermante '}' manquante.")
        return False, "Expected '}' to close the repeat block"




   
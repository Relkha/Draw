# A Python parser for processing Draw++ commands using a JSON-based syntax definition
import json

# Load keywords from keywords.json
with open("keywords.json") as f:
    keywords_data = json.load(f)

commands = keywords_data["commands"]
loops = keywords_data["loops"]
conditionals = keywords_data["conditionals"]
functions = keywords_data["function"]
shapes = keywords_data["shapes"]

class Parser:
    """
    A parser class for analyzing and validating Draw++ commands.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.last_conditional = None

    def _current_token(self):
        """
        Returns the current token.
        """
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _advance(self):
        """
        Advances to the next token.
        """
        if self.position < len(self.tokens):
            self.position += 1

    def _match(self, token_type):
        """
        Checks if the current token matches the expected type.
        """
        current = self._current_token()
        if current:
            current_type, current_value = current

            if token_type == "CONDITION":
                if current_type in ["CONDITION", "SHAPE"]:
                    self._advance()
                    return True

            if token_type == "NUMBER_OR_VARIABLE":
                if current_type in ["NUMBER", "VARIABLE"]:
                    self._advance()
                    return True

            if current_type == token_type:
                self._advance()
                return True

        return False

    def parse(self):
        """
        Main method to parse the tokens.
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
                return True, None
            else:
                return False, f"Unexpected token: {current[0]}"
        return True, None

    def _parse_function(self, keyword):
        """
        Parses a function declaration.
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
        Checks constraints for a specific command argument.
        """
        constraints = commands.get(command_name, {}).get("constraints", {})
        arg_constraints = constraints.get("args", {})

        if token[0] == "NUMBER":
            try:
                value = int(token[1])
            except ValueError:
                return False, f"Invalid number format: {token[1]}"

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
        Parses a simple command based on keywords.json.
        """
        command = self._current_token()
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
            if current_token and current_token[0] == "RBRACE":
                return True, None
            if not current_token or not self._match(expected_type):
                return False, f"Expected {expected_type} after {command_name}"

            is_valid, error_message = self._check_constraints(current_token, command_name, i)
            if not is_valid:
                return False, error_message

        if self._current_token() and self._current_token()[0] == "SEMICOLON":
            self._advance()

        return True, None

    def _parse_conditional(self, keyword):
        """
        Parses a conditional statement (if/else).
        """
        if keyword not in conditionals:
            return False, f"Unknown conditional: {keyword}"

        self.last_conditional = keyword
        self._advance()

        expected_args = conditionals[keyword]["args"]

        for expected_type in expected_args:
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            current_token = self._current_token()

            if expected_type == "CONDITION":
                if current_token and current_token[0] in ["CONDITION", "SHAPE"]:
                    self._advance()
                    continue
                else:
                    return False, f"Expected CONDITION or SHAPE, but found {current_token}"

            elif expected_type == "block_content":
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
                        return False, f"Unexpected token in block_content: {current_token}"

                    if not is_valid:
                        return False, error

            elif not self._match(expected_type):
                return False, f"Expected {expected_type}, but found {current_token}"

        return True, None

    def _parse_loop(self, keyword):
        """
        Parses a loop statement (e.g., repeat).
        """
        if keyword not in loops:
            return False, f"Unknown loop: {keyword}"

        self._advance()

        expected_args = loops[keyword]["args"]
        for expected_type in expected_args:
            while self._current_token() and self._current_token()[0] == "WHITESPACE":
                self._advance()

            if expected_type in "block_content":
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
                        return False, f"Unexpected token in loop block: {current_token}"

                    if not is_valid:
                        return False, error

            elif not self._match(expected_type):
                return False, f"Expected {expected_type} in {keyword} declaration"

        current_token = self._current_token()
        if current_token and current_token[0] == "RBRACE":
            return True, None

        return False, "Expected '}' to close the repeat block"

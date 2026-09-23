from tokenType import TokenType

# creates a token object with a type, lexeme, and line number for each token
class Token:
    # constructor
    def __init__(self, token_type, lexeme, line):
        self._type = token_type
        self._lexeme = lexeme
        self._line = line

    # getters
    def get_type(self):
        return self._type

    def get_lexeme(self):
        return self._lexeme

    def get_line(self):
        return self._line

    # print logic 
    def __str__(self):
        if self._type == TokenType.IDENTIFIER or self._type == TokenType.INTEGER_LITERAL or self._type == TokenType.REAL_LITERAL:
            return self._type + "(" + self._lexeme + ")"
        return self._type

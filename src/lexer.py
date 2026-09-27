from token import Token
from tokenType import TokenType

class LexicalError(Exception):
    pass

# takes in a statement and returns a list of tokens
class Lexer:

    KEYWORDS = {
        "int": TokenType.INT,
        "real": TokenType.REAL,
        "print": TokenType.PRINT
    }

    SINGLE_CHARS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MULTIPLY,
        "/": TokenType.DIVIDE,
        "=": TokenType.ASSIGN,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        ";": TokenType.SEMICOLON
    }

    # constructor
    def __init__(self, source_text):
        self._source = source_text
        self._index = 0
        self._line = 1
        self._tokens = []

    # walks the source text once and builds a list of Token objects
    def tokenize(self):
        self._index = 0
        self._line = 1
        self._tokens = []

        while not self._is_at_end():
            self._skip_whitespace()
            if self._is_at_end():
                break

            current_char = self._current()

            if current_char.isalpha():
                self._read_word()
            elif current_char.isdigit():
                self._read_number()
            elif current_char in Lexer.SINGLE_CHARS:
                self._add_token(Lexer.SINGLE_CHARS[current_char], current_char)
                self._advance()
            else:
                raise LexicalError("Lexical Error on line " + str(self._line) + 
                ": Unknown character '" + current_char + "'")

        return self._tokens

    # getters
    def get_tokens(self) -> list[Token]:
        return self._tokens

    # for when the index is at the end of the source text
    def _is_at_end(self) -> bool:
        return self._index >= len(self._source)

    # returns the character at the current index
    def _current(self) -> str:
        if self._is_at_end():
            return ""
        return self._source[self._index]

    # looks one character ahead without moving the index
    def _peek(self) -> str:
        next_index = self._index + 1
        if next_index >= len(self._source):
            return ""
        return self._source[next_index]

    # consumes the current character and moves the index forward
    def _advance(self) -> str:
        current_char = self._current()
        self._index += 1
        return current_char

    # skips spaces, tabs, and newlines, and updates the line number
    def _skip_whitespace(self) -> None:
        while not self._is_at_end() and self._current() in " \t\r\n":
            if self._current() == "\n":
                self._line += 1
            self._advance()

    # reads a keyword or identifier starting with a letter
    def _read_word(self) -> None:
        start_line = self._line
        lexeme = ""

        while not self._is_at_end() and (self._current().isalnum() or self._current() == "_"):
            lexeme += self._advance()

        if lexeme in Lexer.KEYWORDS:
            token_type = Lexer.KEYWORDS[lexeme]
        else:
            token_type = TokenType.IDENTIFIER

        self._add_token(token_type, lexeme, start_line)

    # reads an integer or real literal starting with a digit
    def _read_number(self) -> None:
        start_line = self._line
        lexeme = ""

        while not self._is_at_end() and self._current().isdigit():
            lexeme += self._advance()

        if self._current() == ".":
            if not self._peek().isdigit():
                raise LexicalError("Lexical Error on line " + str(start_line) + ": Invalid real literal '" + lexeme + ".'")

            lexeme += self._advance()
            while not self._is_at_end() and self._current().isdigit():
                lexeme += self._advance()
            self._add_token(TokenType.REAL_LITERAL, lexeme, start_line)
        else:
            self._add_token(TokenType.INTEGER_LITERAL, lexeme, start_line)

    # creates a Token and appends it to the token list
    def _add_token(self, token_type: TokenType, lexeme: str, line: int = None) -> None:
        if line is None:
            line = self._line
        self._tokens.append(Token(token_type, lexeme, line))

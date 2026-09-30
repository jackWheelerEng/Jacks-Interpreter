"""
Implements a recursive-descent parser with one method per grammar rule

Uses iterative loops to implement PEMDAS

The parser builds an AST as it iterates through 
each token, verifies that every token is parsed, 
and reports when there is an error parsing, or 
if there are any grammar violations

--------THIS FILE REQUIRES THE LEXER, TOKEN, TOKENTYPE, AND AST_NODE FILES TO RUN--------
"""

from token import Token
from tokenType import TokenType
from ast_nodes import (
    Program,
    Declaration,
    Assignment,
    PrintStatement,
    BinaryOp,
    Identifier,
    IntegerLiteral,
    RealLiteral,
)


class SyntaxErrorMiniLang(Exception):
    """Raised for any grammar violation. Carries a line number so the
    driver can print 'Syntax Error on line N: <message>' per Section 12."""

    def __init__(self, message: str, line: int):
        self.line = line
        self.message = message
        super().__init__(f"Syntax Error on line {line}: {message}")


_TYPE_TOKENS = (TokenType.INT, TokenType.REAL)
_ADD_OPS = (TokenType.PLUS, TokenType.MINUS)
_MUL_OPS = (TokenType.MULTIPLY, TokenType.DIVIDE)

# Token types whose lexeme IS the human-readable text (keywords,
# identifiers, literals) -- everything else is a fixed symbol.
_LEXEME_IS_DISPLAY_TEXT = (
    TokenType.IDENTIFIER,
    TokenType.INTEGER_LITERAL,
    TokenType.REAL_LITERAL,
    TokenType.INT,
    TokenType.REAL,
    TokenType.PRINT,
)


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)

    #Helpers for keeping track of position in the list of tokens while parsing

    def _at_end(self) -> bool:
        return self.pos >= self.length

    def _current(self):
        """Returns the current Token, or None if we've run off the end
        of the token list."""
        if self._at_end():
            return None
        return self.tokens[self.pos]

    def _current_line(self) -> int:
        """The line an error is reported from."""
        tok = self._current()
        if tok is not None:
            return tok.get_line()
        if self.tokens:
            return self.tokens[-1].get_line()
        return 1

    def _check(self, *types) -> bool:
        tok = self._current()
        return tok is not None and tok.get_type() in types

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _expect(self, type_, expected_desc: str) -> Token:
        """Take in a string token, or raise error"""
        if self._check(type_):
            return self._advance()
        raise SyntaxErrorMiniLang(
            f"Expected {expected_desc} but found {self._describe(self._current())}",
            self._current_line(),
        )

    #End Token Helpers

    @staticmethod
    def _describe(tok) -> str:
        if tok is None:
            return "end of input"
        t = tok.get_type()
        if t in _LEXEME_IS_DISPLAY_TEXT:
            return f"'{tok.get_lexeme()}'"
        symbol_map = {
            TokenType.PLUS: "+", TokenType.MINUS: "-",
            TokenType.MULTIPLY: "*", TokenType.DIVIDE: "/",
            TokenType.ASSIGN: "=", TokenType.LEFT_PAREN: "(",
            TokenType.RIGHT_PAREN: ")", TokenType.SEMICOLON: ";",
        }
        return f"'{symbol_map.get(t, t)}'"
    

    # Methods associated for each grammar rule

    def parse_program(self) -> Program:
        """Parses statements until end of token list"""

        statements = []
        while not self._at_end():
            statements.append(self.parse_statement())
        return Program(statements, line=1)
    

    def parse_statement(self):
        """Displays the token declaration, prints, 
        and/or Identifier when parsed"""

        if self._check(*_TYPE_TOKENS):
            return self.parse_declaration()
        if self._check(TokenType.PRINT):
            return self.parse_print_statement()
        if self._check(TokenType.IDENTIFIER):
            return self.parse_assignment()

        raise SyntaxErrorMiniLang(
            "Expected a declaration, assignment, or print statement but found "
            f"{self._describe(self._current())}",
            self._current_line(),
        )
    

    def parse_declaration(self) -> Declaration:
        """<declaration> -> <type> identifier ";" """
        type_tok = self._advance()  # INT or REAL checked by caller
        var_type = type_tok.get_lexeme()

        name_tok = self._expect(TokenType.IDENTIFIER, "a variable name")
        self._expect(TokenType.SEMICOLON, "';' after variable declaration")

        return Declaration(var_type, name_tok.get_lexeme(), line=type_tok.get_line())
    

    def parse_assignment(self) -> Assignment:
        """<assignment> -> identifier "=" <expression> ";" """
        name_tok = self._advance()  # IDENTIFIER checked by caller
        self._expect(TokenType.ASSIGN, "'=' in assignment")

        expr = self.parse_expression()
        self._expect(TokenType.SEMICOLON, "';' after assignment")

        return Assignment(name_tok.get_lexeme(), expr, line=name_tok.get_line())
    

    def parse_print_statement(self) -> PrintStatement:
       
        print_tok = self._advance()  # PRINT checked by caller
        self._expect(TokenType.LEFT_PAREN, "'(' after 'print'")

        expr = self.parse_expression()
        self._expect(TokenType.RIGHT_PAREN, "')' after print expression")
        self._expect(TokenType.SEMICOLON, "';' after print statement")

        return PrintStatement(expr, line=print_tok.get_line())
    

    def parse_expression(self):
        """Sets up the AST from left ro right"""
        node = self.parse_term()
        while self._check(*_ADD_OPS):
            op_tok = self._advance()
            right = self.parse_term()
            op = "+" if op_tok.get_type() == TokenType.PLUS else "-"
            node = BinaryOp(op, node, right, line=op_tok.get_line())
        return node
    

    def parse_term(self):
        """Uses same loop as parse_expression, except
          one level higher to implement PEMDAS correctly"""
        node = self.parse_factor()
        while self._check(*_MUL_OPS):
            op_tok = self._advance()
            right = self.parse_factor()
            op = "*" if op_tok.get_type() == TokenType.MULTIPLY else "/"
            node = BinaryOp(op, node, right, line=op_tok.get_line())
            
        return node
    


    def parse_factor(self):
        """Takes literal strings and sets them to INT or FLOAT"""
        tok = self._current()
        if tok is None:
            raise SyntaxErrorMiniLang(
                "Expected an identifier, number, or '(' but found end of input",
                self._current_line(),
            )

        t = tok.get_type()

        if t == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(tok.get_lexeme(), line=tok.get_line())

        if t == TokenType.INTEGER_LITERAL:
            self._advance()
            return IntegerLiteral(int(tok.get_lexeme()), line=tok.get_line())

        if t == TokenType.REAL_LITERAL:
            self._advance()
            return RealLiteral(float(tok.get_lexeme()), line=tok.get_line())

        if t == TokenType.LEFT_PAREN:
            self._advance()
            expr = self.parse_expression()
            self._expect(TokenType.RIGHT_PAREN, "')' to close '('")
            return expr

        raise SyntaxErrorMiniLang(
            f"Expected an identifier, number, or '(' but found {self._describe(tok)}",
            tok.get_line(),
        )


def parse(tokens: list) -> Program:
    """Convenience entry point: parse a full token list into a Program AST."""
    return Parser(tokens).parse_program()

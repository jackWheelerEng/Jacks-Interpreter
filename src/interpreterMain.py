import sys
from sourceFileReader import SourceFileReader
from lexer import Lexer, LexicalError
from token import Token
from parser import parse, SyntaxErrorMiniLang
from syntaxTree import SyntaxTree
from semanticAnalyzer import analyze, SemanticError
from interpreter import Interpreter, RuntimeErrorMiniLang


def display_loaded_source(source_reader: SourceFileReader) -> None:
    print("Loaded source file: " + source_reader.get_file_name())
    print("------")

    source_lines = source_reader.get_source_lines()
    for i in range(len(source_lines)):
        print(str(i + 1) + " | " + source_lines[i])

    print("------")
    print(str(source_reader.get_line_count()) + " lines read.")


def display_tokens(tokens: list[Token]) -> None:
    print("TOKENS")
    print("------")
    for token in tokens:
        print(token)


def display_syntax_tree(syntax_tree: SyntaxTree):
    print("SYNTAX TREE")
    print("------")
    syntax_tree.printTree()


def display_symbol_table(symbol_table):
    print("SYMBOL TABLE")
    print("------")
    print(symbol_table.display())


def main():
    args = sys.argv[1:]
    debug = "--debug" in args
    if debug:
        args = [arg for arg in args if arg != "--debug"]

    if len(args) < 1:
        print("Usage: python interpreterMain.py <source-file.mini> [--debug]")
        return

    file_name = args[0]
    source_reader = SourceFileReader()

    try:
        source_reader.read_from_file(file_name)
    except OSError as e:
        print("Error: " + str(e))
        return

    if debug:
        display_loaded_source(source_reader)

    lexer = Lexer(source_reader.get_source_text())
    try:
        tokens = lexer.tokenize()
    except LexicalError as e:
        print(str(e))
        return

    if debug:
        print()
        display_tokens(tokens)

    try:
        program = parse(tokens)
    except SyntaxErrorMiniLang as e:
        print(str(e))
        return

    if debug:
        syntax_tree = SyntaxTree(program)
        print()
        display_syntax_tree(syntax_tree)

    try:
        symbol_table = analyze(program)
    except SemanticError as e:
        print(str(e))
        return

    interpreter = Interpreter(symbol_table)
    if debug:
        print()
        print("PROGRAM OUTPUT")
        print("------")

    try:
        output = interpreter.run(program)
    except RuntimeErrorMiniLang as e:
        print(str(e))
        return

    if debug:
        if not output:
            print("(none)")
        print()
        display_symbol_table(symbol_table)


if __name__ == "__main__":
    main()

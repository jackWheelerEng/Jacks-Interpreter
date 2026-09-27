import sys
from sourceFileReader import SourceFileReader
from lexer import Lexer, LexicalError
from token import Token


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


def main():
    if len(sys.argv) < 2:
        print("Usage: python interpreterMain.py <source-file.mini>")
        return

    file_name = sys.argv[1]
    source_reader = SourceFileReader()

    try:
        source_reader.read_from_file(file_name)
    except OSError as e:
        print("Error: " + str(e))
        return

    display_loaded_source(source_reader)

    lexer = Lexer(source_reader.get_source_text())
    try:
        tokens = lexer.tokenize()
    except LexicalError as e:
        print(str(e))
        return

    print()
    display_tokens(tokens)


if __name__ == "__main__":
    main()

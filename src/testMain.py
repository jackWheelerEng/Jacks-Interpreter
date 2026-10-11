import sys
 
from lexer import Lexer, LexicalError
from parser import parse, SyntaxErrorMiniLang
from semanticAnalyzer import analyze, SemanticError
from interpreter import Interpreter, RuntimeErrorMiniLang
 
 
def run(path: str, debug: bool) -> int:
    # Read the source file
    try:
        with open(path, "r") as f:
            source = f.read()
    except OSError as e:
        print(f"Error: could not read file '{path}': {e}")
        return 1
 
    # Lexical analysis
    try:
        tokens = Lexer(source).tokenize()
    except LexicalError as e:
        print(str(e))
        return 1
 
    if debug:
        print("TOKENS")
        print("------")
        for tok in tokens:
            print(tok)
        print()
 
    # Syntax analysis section
    try:
        ast = parse(tokens)
    except SyntaxErrorMiniLang as e:
        print(str(e))
        return 1
 
    if debug:
        print("AST / PARSE TREE")
        print("----------------")
        print(ast.pretty())
        print()
 
    # Static semantic analysis section
    try:
        symbol_table = analyze(ast)
    except SemanticError as e:
        print(str(e))
        return 1
 
    # Interpreter execution section
    interpreter = Interpreter(symbol_table)
    if debug:
        print("PROGRAM OUTPUT")
        print("--------------")
    try:
        interpreter.run(ast)
    except RuntimeErrorMiniLang as e:
        print(str(e))
        return 1
 
    # symbol table dump comes after execution, since
    # final variable values aren't known until the program has run
    if debug:
        print()
        print("SYMBOL TABLE")
        print("------------")
        print(symbol_table.display())
 
    return 0
 
 
def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file.mini> [--debug]")
        return 1
 
    source_path = sys.argv[1]
    debug_mode = "--debug" in sys.argv[2:]
    return run(source_path, debug_mode)
 
 
if __name__ == "__main__":
    sys.exit(main())

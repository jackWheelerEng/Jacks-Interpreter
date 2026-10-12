# Jacks Interpreter

MiniLang interpreter for CS 3210 Project 2.

## Requirements

- Python 3.8 or later (no third-party packages required — everything
  used is Python's standard library)

Check your version:

```
python3 --version
```

## Project files

All files below must stay together in the same folder; `main.py` imports
the others directly.

```
main.py              <- run this file
lexer.py
token.py
tokenType.py
ast_nodes.py
parser.py
semantic_analyzer.py
interpreter.py
```

## Build

No build step required 
(MiniLang programs are interpreted
directly from source each time you run `main.py`.)

## How to run

```
python3 main.py <path_to_program.mini>
```

Example:

```
python3 main.py tests/end_to_end/example.mini
```

For a valid program, this prints exactly what the program's own
`print(...)` statements produce. For an invalid program, it prints one
line identifying the error (Lexical, Syntax, Semantic, or Runtime) and
exits with a non-zero status.

## Debug mode

Add `--debug` as a second argument to additionally print the token
stream, the parsed AST, the program's output, and the final symbol
table:

```
python3 main.py tests/end_to_end/example.mini --debug
```

## Running the test suite

Sample `.mini` programs are provided under `tests/`. Run any of them
the same way:

```
python3 main.py tests/section14/test01_basic_declaration_int.mini
```


Pass any MiniLang source file as the first argument. If the file is missing or cannot be opened, the program prints an error and exits without a stack trace.

---

This codebase was made with assistance from Grok 4.6.

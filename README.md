# Jacks Interpreter

MiniLang interpreter for CS 3210 Project 2.

## Current stage

This repository currently reads a MiniLang source file and holds the text for a later lexical analyzer. Tokenizing, parsing, and execution are not implemented yet.

## How to run

From the project root:

```
python src/interpreterMain.py examples/program1.mini
```

Pass any MiniLang source file as the first argument. If the file is missing or cannot be opened, the program prints an error and exits without a stack trace.

"""
This program takes the AST created by the parser and 
verifies that there are no violations to the miniLang 
grammar rules. 

"""

from ast_nodes import (
    Declaration,
    Assignment,
    PrintStatement,
    BinaryOp,
    Identifier,
    IntegerLiteral,
    RealLiteral,
)


class SemanticError(Exception):
    """Raised for rule violations and prints the line 
    the violation is located at."""

    def __init__(self, message: str, line: int):
        self.line = line
        self.message = message
        super().__init__(f"Semantic Error on line {line}: {message}")


class SymbolTableEntry:
    __slots__ = ("name", "var_type", "initialized", "value")

    def __init__(self, name: str, var_type: str):
        self.name = name
        self.var_type = var_type        # "int" | "real"
        self.initialized = False        # Section 9: "Initialized"
        self.value = None               # Section 9: "Value" (filled in by
                                         # the interpreter stage, if present)


class SymbolTable:
    """Tracks declared variables in the order they are declared in. """

    def __init__(self):
        self._entries: dict[str, SymbolTableEntry] = {}

    def declare(self, name: str, var_type: str) -> None:
        self._entries[name] = SymbolTableEntry(name, var_type)

    def is_declared(self, name: str) -> bool:
        return name in self._entries

    def get(self, name: str) -> SymbolTableEntry:
        return self._entries[name]

    def entries(self):
        """All entries, in declaration order."""
        return self._entries.values()

    def display(self) -> str:
        """Dump for debug/display mode."""
        if not self._entries:
            return "(empty)"
        lines = [f"{'NAME':<12}{'TYPE':<6}{'INIT':<6}{'VALUE'}"]
        for entry in self._entries.values():
            value_str = "-" if entry.value is None else str(entry.value)
            lines.append(
                f"{entry.name:<12}{entry.var_type:<6}"
                f"{('yes' if entry.initialized else 'no'):<6}{value_str}"
            )

        return "\n".join(lines)


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, program) -> SymbolTable:
        """Checks the semantic rules int he parser.
        Returns the populated symbol table if successful;"""
        for statement in program.statements:
            self._check_statement(statement)
        return self.symbol_table

    def _check_statement(self, stmt) -> None:
        if isinstance(stmt, Declaration):
            self._check_declaration(stmt)

        elif isinstance(stmt, Assignment):
            self._check_assignment(stmt)

        elif isinstance(stmt, PrintStatement):
            self._check_print(stmt)

        else:  #parser should never produce this
            raise SemanticError(
                f"Internal error: unknown statement node {type(stmt).__name__}",
                stmt.line,
            )

    def _check_declaration(self, decl: Declaration) -> None:
        """Rule 2 - Duplicate Declarations Are Not Allowed."""
        if self.symbol_table.is_declared(decl.name):
            raise SemanticError(
                f"Variable '{decl.name}' is already declared.", decl.line
            )
        self.symbol_table.declare(decl.name, decl.var_type)


    def _check_assignment(self, assign: Assignment) -> None:
        """Checks rule 1 and rule 3 and marks the target as initialized"""
        if not self.symbol_table.is_declared(assign.name):
            raise SemanticError(
                f"Variable '{assign.name}' is not declared.", assign.line
            )

        expr_type = self._check_expression(assign.expression)
        entry = self.symbol_table.get(assign.name)

        #Rule 3
        if entry.var_type == "int" and expr_type == "real":
            raise SemanticError(
                f"Cannot assign real value to int variable '{assign.name}'.",
                assign.line,
            )

        entry.initialized = True

    def _check_print(self, pr: PrintStatement) -> None:
        """Checks print statements against rules where applicable"""
        self._check_expression(pr.expression)



    #expression-level checks

    def _check_expression(self, node) -> str:
        """Type-checks an expression subtree and
          returns type ("int" or "real")"""
        if isinstance(node, IntegerLiteral):
            return "int"

        if isinstance(node, RealLiteral):
            return "real"

        if isinstance(node, Identifier):
            if not self.symbol_table.is_declared(node.name):
                raise SemanticError(
                    f"Variable '{node.name}' is not declared.", node.line
                )
            entry = self.symbol_table.get(node.name)
            if not entry.initialized:
                raise SemanticError(
                    f"Variable '{node.name}' is used before being initialized.",
                    node.line,
                )
            return entry.var_type

        if isinstance(node, BinaryOp):
            left_type = self._check_expression(node.left)
            right_type = self._check_expression(node.right)

            #Rule 4: int op int -> int; any real operand -> real.
            return "real" if "real" in (left_type, right_type) else "int"


        raise SemanticError( #parser should never produce this
            f"Internal error: unknown expression node {type(node).__name__}",
            node.line,
        )


def analyze(program) -> SymbolTable:
    """Convenience entry point, mirroring parser.parse()."""
    return SemanticAnalyzer().analyze(program)

from ast_nodes import (
    Declaration,
    Assignment,
    PrintStatement,
    BinaryOp,
    Identifier,
    IntegerLiteral,
    RealLiteral,
)


class RuntimeErrorMiniLang(Exception):
    def __init__(self, message, line):
        self.line = line
        self.message = message
        super().__init__("Runtime Error on line " + str(line) + ": " + message)


class Interpreter:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.output = []

    # walks the program and runs each statement in order
    def run(self, program):
        self.output = []
        for statement in program.statements:
            self._run_statement(statement)
        return self.output

    def _run_statement(self, stmt):
        if isinstance(stmt, Declaration):
            return
        if isinstance(stmt, Assignment):
            self._run_assignment(stmt)
            return
        if isinstance(stmt, PrintStatement):
            self._run_print(stmt)

    # evaluates the right side and stores it in the symbol table
    def _run_assignment(self, assign):
        value = self._eval(assign.expression)
        entry = self.symbol_table.get(assign.name)
        if entry.var_type == "real" and isinstance(value, int):
            value = float(value)
        entry.value = value
        entry.initialized = True

    def _run_print(self, pr):
        value = self._eval(pr.expression)
        text = self._format_value(value)
        self.output.append(text)
        print(text)

    # evaluates an expression node to a number
    def _eval(self, node):
        if isinstance(node, IntegerLiteral):
            return node.value
        if isinstance(node, RealLiteral):
            return node.value
        if isinstance(node, Identifier):
            return self.symbol_table.get(node.name).value
        if isinstance(node, BinaryOp):
            return self._eval_binary(node)
        return None

    # evaluates a binary operation node to a number
    def _eval_binary(self, node):
        left = self._eval(node.left)
        right = self._eval(node.right)

        if node.op == "/" and right == 0:
            raise RuntimeErrorMiniLang("Division by zero.", node.line)

        both_int = isinstance(left, int) and isinstance(right, int)
        if node.op == "+":
            result = left + right
        elif node.op == "-":
            result = left - right
        elif node.op == "*":
            result = left * right
        elif both_int:
            result = left // right
        else:
            result = left / right

        if both_int:
            return int(result)
        return float(result)

    def _format_value(self, value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

# shared fields and print helpers for every AST node
class ASTNode:
    def __init__(self, line):
        self.line = line

    # text shown for this node in the syntax tree
    def label(self):
        return type(self).__name__

    # child nodes used when building the printed tree
    def children(self):
        return []

    def __str__(self):
        return self.label()


# root node that holds every statement in the program
class Program(ASTNode):
    
    def __init__(self, statements, line=1):
        super().__init__(line)
        self.statements = statements

    def label(self):
        return "Program"

    def children(self):
        return self.statements


# a variable declaration such as int width;
class Declaration(ASTNode):
    
    def __init__(self, var_type, name, line):
        super().__init__(line)
        self.var_type = var_type
        self.name = name

    def label(self):
        return "Declaration(" + self.var_type + " " + self.name + ")"


# an assignment such as width = 10;
class Assignment(ASTNode):
    
    def __init__(self, name, expression, line):
        super().__init__(line)
        self.name = name
        self.expression = expression

    def label(self):
        return "Assignment"

    def children(self):
        return [Identifier(self.name, self.line), self.expression]


# a print statement such as print(area);
class PrintStatement(ASTNode):
    
    def __init__(self, expression, line):
        super().__init__(line)
        self.expression = expression

    def label(self):
        return "Print"

    def children(self):
        return [self.expression]


# a binary operator with a left and right child
class BinaryOp(ASTNode):
    
    def __init__(self, op, left, right, line):
        super().__init__(line)
        self.op = op
        self.left = left
        self.right = right

    def label(self):
        return "Binary(" + self.op + ")"

    def children(self):
        return [self.left, self.right]


# a variable name used in an expression
class Identifier(ASTNode):
    
    def __init__(self, name, line):
        super().__init__(line)
        self.name = name

    def label(self):
        return "Identifier(" + self.name + ")"


# an integer literal such as 10
class IntegerLiteral(ASTNode):
    
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value

    def label(self):
        return "Integer(" + str(self.value) + ")"


# a real literal such as 10.5
class RealLiteral(ASTNode):
    
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value

    def label(self):
        return "Real(" + str(self.value) + ")"

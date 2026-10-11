from anytree import Node, RenderTree


class SyntaxTree:
    def __init__(self, program=None):
        self.root = None
        if program is not None:
            self.build(program)

    def build(self, program):
        self.root = self._to_anytree(program)

    def addNode(self, node: Node):
        self.root = node

    def getRoot(self):
        return self.root

    def printTree(self):
        if self.root is None:
            print("(empty)")
            return

        for prefix, _, node in RenderTree(self.root):
            print(prefix + node.name)

    def _to_anytree(self, ast_node, parent=None):
        tree_node = Node(ast_node.label(), parent=parent)
        for child in ast_node.children():
            self._to_anytree(child, tree_node)
        return tree_node

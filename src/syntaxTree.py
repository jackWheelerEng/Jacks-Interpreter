from token import Token
from anytree import Node

class SyntaxTree:
    
    def __init__(self):
        self.root = None

    def addNode(self, node: Node):
        self.root = node

    def getRoot(self):
        return self.root

    def pringTree(self):
        print(self.root)

    def printTree(self):
        print(self.root.printTree())



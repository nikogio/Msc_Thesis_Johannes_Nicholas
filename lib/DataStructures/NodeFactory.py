from manim import *
from DataStructures.Node import Node

class NodeFactory:
    def __init__(self):
        return

    def create_node(self, value, radius):
        node = Node(value,radius)
        return node
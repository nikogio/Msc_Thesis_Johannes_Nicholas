from manim import *
from DataStructures.Node import Node

class NodeExample(Scene):  
    def construct(self):

        # create the slot
        node = Node('a')
        self.add(node)
        node1 = Node('b').shift(RIGHT)
        self.play(Create(node1))
        self.play(node1.animate.scale(0.5))
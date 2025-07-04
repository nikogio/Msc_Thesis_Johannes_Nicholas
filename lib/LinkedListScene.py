from manim import *
from DataStructures.LinkedList import LinkedList

class LinkedListAdding(Scene):
    def construct(self):
        h = LinkedList(self)
        h.add_value('a')
        h.add_value('b')
        h.add_value('c')
        h.add_value('d')
        h.search('c')


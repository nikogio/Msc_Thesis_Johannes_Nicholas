from manim import *
from DataStructures.HashTable import HashTable

class HashTableScene(Scene):
    def construct(self):
        h = HashTable(self,side_length=1,size=4)
        h.add_value('a')
        h.add_value('b')
        h.add_value('c')
        h.add_value('e')
        h.add_value('i')
        h.turn_yellow()
        self.wait
class HashTableScene2(Scene):
    def construct(self):
        h = HashTable(self,side_length=1,size=4,resizing=True,max_ll_length=3)
        h.add_value('a')
        h.add_value('b')
        h.add_value('c')
        h.add_value('d')
        h.add_value('e')
        h.add_value('h')
        h.add_value('i')
        h.add_value('j')
        h.add_value('k')
        h.add_value('m')

class Test(Scene):
    def construct(self):
        h = HashTable(self,side_length=1,size=4,resizing=True,max_ll_length=1)
        h.turn_grey()

        
from manim import *
from DataStructures.HTMemory import HTMemory
from DataStructures.Array import Array

#this class is to render an animation where both hash table and memory are displayed

class HTMem(Scene):
    def construct(self):
        ht = HTMemory(scene=self,resizing=True)
        self.wait()
        ht.add_value('a')
        ht.add_value('b')
        ht.add_value('c')
        ht.add_value('e')
        ht.add_value('i')
        ht.add_value('m')
        self.wait()
        
class Colors(Scene):
    def construct(self):
        ht = HTMemory(scene=self,resizing=True,size=4,color_coding=True)
        ht.add_value('a')
        ht.add_value('e')
        ht.add_value('i')
        ht.add_value('m')
        self.wait()
        
class TestGr(Scene):
    def construct(self):
        htm = HTMemory(scene=self,resizing=True,size=4,color_coding=True)
        htm.add_value('a')
        htm.hash_table.turn_grey()
        
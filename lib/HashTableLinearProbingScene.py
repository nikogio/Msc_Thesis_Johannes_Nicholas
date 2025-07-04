from manim import *
from DataStructures.HashTableLinearProbing import HashTableLinearProbing

class HTLPExample(Scene):
     def construct(self):
          ht = HashTableLinearProbing(self)
          ht.insert('a')
          ht.insert('i')
          ht.insert('b')
          ht.insert('c')
          ht.insert('d')

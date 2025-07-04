from manim import *
from DataStructures.ResizingArrayMemory import RAMemory

class RAMemScene(Scene):
    def construct(self):
        s = RAMemory(self,'stack')
        s.add('a')
        s.add('a')
        s.add('a')
        s.add('a')
        s.add('a')
        s.add('a')
        s.add('a')
        s.add('a')
        s.add('a')
        s.add('a')

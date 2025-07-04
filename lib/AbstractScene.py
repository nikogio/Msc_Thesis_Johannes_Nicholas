from manim import *
from DataStructures.StackAbstract import StackAbstract

class StackAbstractScene(Scene):
    def construct(self):
        s = StackAbstract(scene=self)
        s.push('a')

class BagAbstractScene(Scene):
    def construct(self):
        s = BagAbstract(scene=self)
        s.put('a')
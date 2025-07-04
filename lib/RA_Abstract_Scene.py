from manim import *
from DataStructures.ResizingArray import Stack
from DataStructures.StackAbstract import StackAbstract

class Stack_Abstract_RA_Scene(Scene):
    def construct(self):
        upper_rec = Rectangle(width=14,height=4).move_to([0,1.9,0])
        lower_rec = Rectangle(width=14,height=4).move_to([0,-2,0])
        self.array_stack = Stack(scene=self,screen_rectangle=upper_rec)
        self.abstract_stack = StackAbstract(scene=self,location=[0,-2.2,0],height=3.5)

        self.add(self.array_stack, self.abstract_stack)
        self.push('a')
        self.push('b')
        self.push('c')
        self.push('d')
        self.push('e')
        self.pop()
        self.pop()



    def push(self,val):
        self.array_stack.push(val)
        self.abstract_stack.push(val)

    def pop(self):
        self.array_stack.pop()
        self.abstract_stack.pop()
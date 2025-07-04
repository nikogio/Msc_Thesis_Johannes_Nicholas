from manim import *
from DataStructures.ResizingArray import Stack
from CostGraph.RACostGraph import RACostGraph



class GraphStack(Scene):
    def construct(self):
        vertical_line = Line([0,10,0],[0,-10,0])
        self.add(vertical_line)
        self.AddGraph()
        self.AddStack()
        num = 1
        for i in  range(10):
            self.push(num + i)
        for i in range(4):
            self.pop()
            
    def AddGraph(self):
        self.graph = RACostGraph(self, x_length=5.0, y_length=4.0,center=([-3.5,0,0]))
        
        
    def AddStack(self):
        self.stack = Stack(scene=self,screen_rectangle=Rectangle(height=5,width=6.5).move_to([3.5,0,0]))
        #self.stack.move_to(RIGHT*4)
        
        
        

    def push(self,value):
        self.graph.add_element(True)    
        self.stack.push(value)
        
        
    def pop(self):
         self.graph.add_element(False)
         self.stack.pop()


class CostGraphScene(Scene):
    def construct(self):
        g = RACostGraph(self, x_length=9.0, y_length=6.0,center=([0,0,0]))
        for i in range(35):
            g.add_element(True)
         

from manim import *
import numpy as np
from CostGraph.CostGraphFactory import CostGraphFactory

class RACostGraph(Mobject):
    
    def __init__(self,scene:Scene, x_length:float=12.0, y_length:float=6.0, min_limit:float=0.25,center:float=0.0,**kwargs):
        super().__init__(**kwargs)
        self.dots = []
        self.n = 0 #number of elements in the resizing array
        self.size = 1 #size of the resizing array
        self.scene = scene
        self.object_center = center
        self.min_limit = min_limit
        self.current_y_ticks_list = [10, 20, 30] # Beginning ticks of graph
        self.current_x_ticks_list = [10, 20, 30] # Beginning ticks of graph

        self.factory = CostGraphFactory(x_length, y_length)
        self.axes = self.factory.create_graph( self.current_x_ticks_list,self.current_y_ticks_list)

        self.scene.add(self.axes)
        self.vg = VGroup() # Group for moving objects
        self.vg.add(self.axes)
        self.vg.move_to(self.object_center)
 

    def addDots(self,x, y, color:str="WHITE"):
        dot = Dot(color = color)
        dot.move_to(self.axes.c2p(x, y))
        self.dots.append(dot)
        self.vg.add(dot) # Adding to VGroup so it can be moved with rest of class
        self.scene.play(Create(dot))
            
    def moveDots(self,new_axes):
        oldpositions = [self.axes.p2c(dot.get_center()) for dot in self.dots]
        animations = [ApplyMethod(dot.move_to, new_axes.c2p(*oldposition)) for dot, oldposition in zip(self.dots, oldpositions)]
        #loop through list of dots and move them to new axes
        return animations #return animations to play them later
    

    def add_element(self,
                    add:bool # Is an element being added to the array or removed?
                    ):
        
        # Calculating action cost
        cost = 0
        if add: 
            if self.n == self.size: # The array is full upon appending, trigger enlarge resizing.
                cost = 4*self.n+1
                self.size *=2
            else:
                cost = 1
       
        else: # Not appending, so removing
            if self.n/self.size == self.min_limit: # It triggers a shrinking resizing
                cost = 4*self.n+1
                self.size /=2
            else:
                cost = 1
        # Finished calculating cost.

        # Updating n
        if add:
             self.n+=1
        else:
             self.n-=1
        # Done updating n

        # Checking for resizing needs
        y_needs_resize = False
        x_needs_resize = False
        if self.current_y_ticks_list[-1]< cost:
             y_needs_resize = True
        if self.current_x_ticks_list[-1]== len(self.dots):
             x_needs_resize = True
        # Finished checking for resizing needs.

        # Setting up for dot
        x_coord = len(self.dots)+1
        y_coord = cost
        color = "GREEN"
        if cost>1:
             color="RED"
        
                 
        if not x_needs_resize and not y_needs_resize: # Adding a dot with no resizing
             self.addDots(x_coord,y_coord,color)
        else:   
            smaller_axes = self.factory.create_graph(self.current_x_ticks_list,
                                                   self.current_y_ticks_list,
                                                   resize_x=x_needs_resize,
                                                   resize_y=y_needs_resize)
            smaller_axes.move_to(self.object_center)

            dot_moving_animation = self.moveDots(smaller_axes)
            self.scene.play(AnimationGroup(
                *dot_moving_animation,
                ReplacementTransform(self.axes, smaller_axes)))
            
            # Clean up of fields to new values.
            self.current_y_ticks_list = smaller_axes.y_axis.numbers_to_include
            self.current_x_ticks_list = smaller_axes.x_axis.numbers_to_include
            self.vg.remove(self.axes)
            self.axes = smaller_axes
            self.vg.add(self.axes)

            self.addDots(x_coord,y_coord,color)
            
        
class GraphScene(Scene):
    def construct(self):
        graph = RACostGraph(self)
        graph.add_element(True)
        for i in range(100):
            graph.add_element(True)

class Test_Positioning(Scene):
     def construct(self):
          g = RACostGraph(self)
          g.add_element(True)
          g.add_element(True)
          g.add_element(True)
          g.add_element(True)
          self.play(g.vg.animate.next_to(LEFT*4,buff=0.1))
          for i in range(10):
            g.add_element(True)
    

class ShiftAxes(Scene):
    def construct(self):
        graph = RACostGraph(self, x_length=5.0, y_length=2.0)
        graph.add_element(True)
        for i in range(4):
            graph.add_element(True)
        
        
from manim import *
from DataStructures.BagAbstract import BagAbstract
from DataStructures.QueueAbstract import QueueAbstract
from DataStructures.StackAbstract import StackAbstract

# This is a facade class for the visual implementations of Stack, Bag, Queue and PQ.

class FacadeAbstract():
    def __init__(self,
                type:str,
                scene=Scene,
                **kwargs):
        self.types = ['stack','queue','bag']
        self.type = type.lower()
        if not type in self.types:
            raise ValueError("Data structure type must be: 'stack', 'queue' or 'bag'")
        
        # Setup of underlying data structure.
        if type =='stack':
            self.underlying = StackAbstract(scene=scene,**kwargs)
        elif type == 'queue':
            self.underlying = QueueAbstract(scene=scene,**kwargs)
        else:
            self.underlying = BagAbstract(scene=scene,**kwargs)

    def add(self,value):
        if self.type =='stack':
            self.underlying.push(value)
        elif self.type == 'queue':
            self.underlying.enqueue(value)
        else:
            self.underlying.put(value)

    def remove(self,value):
        if self.type =='stack':
            self.underlying.pop()
        elif self.type == 'queue':
            self.underlying.dequeue()
        else:
            self.underlying.pull(value)
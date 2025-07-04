from manim import *
from DataStructures.ResizingArray import Stack, Bag, Queue
from DataStructures.PriorityQueue import PriorityQueue

# This is a facade class for the visual implementations of Stack, Bag, Queue and PQ.

class FacadeRA():
    def __init__(self,
                RAtype:str,
                side_length: float = 2.0,
                scene=Scene,
                center:np.array= [0,0,0],
                max_oriented:bool = False,
                screen_rectangle: Rectangle = Rectangle(height=8,width=14), # Default is full screen.
                **kwargs):
        self.types = ['stack','queue','bag','priorityqueue','pq','priority queue']
        self.underlying = None # The field for the underlying data structure.
        self.RAtype = RAtype.lower()
        if not RAtype in self.types:
            raise ValueError("Data structure type must be: 'stack', 'queue','bag' or 'priority queue'")
        
        # Setup of underlying data structure.
        if RAtype =='stack':
            self.underlying = Stack(scene=scene,
                                    side_length=side_length,
                                    screen_rectangle=screen_rectangle)
        elif RAtype == 'queue':
            self.underlying = Queue(scene=scene,
                                    side_length=side_length, 
                                    center=center,
                                    screen_rectangle=screen_rectangle)
        elif RAtype == 'bag':
            self.underlying = Bag(scene=scene,
                                  side_length=side_length,
                                  screen_rectangle=screen_rectangle)
        else:
            self.underlying = PriorityQueue(scene=scene,
                                            side_length=side_length,
                                            screen_rectangle=screen_rectangle,
                                            max_oriented=max_oriented)

    def add(self,value):
        resized = False
        if self.RAtype =='stack':
            resized = self.underlying.push(value)
        elif self.RAtype == 'queue':
            resized = self.underlying.enqueue(value)
        elif self.RAtype == 'bag':
            resized = self.underlying.put(value)
        else:
            resized = self.underlying.insert(value)
        return resized

    def remove(self,value):
        if self.RAtype =='stack':
            self.underlying.pop()
        elif self.RAtype == 'queue':
            self.underlying.dequeue()
        elif self.RAtype == 'bag':
            self.underlying.pull()
        else:
            self.underlying.delete_next(value)
        
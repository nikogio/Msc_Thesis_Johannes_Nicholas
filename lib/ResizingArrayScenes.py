from manim import *
from DataStructures.ResizingArray import Stack, Queue, Bag
from DataStructures.FacadeResizingArray import FacadeRA

class StackScene(Scene):
    def construct(self):
        r = Rectangle(height=4,width=14)
        s = Stack(self, size=2,screen_rectangle=r)
        s.push('a')
        s.push('b')
        s.push('c')
        s.push('d')
        s.push('e')
        s.push('f')
        s.push('g')
        s.pop()
        s.pop()
        s.pop()
        s.pop()
        s.pop()
        s.pop()

class QueueExample(Scene):
    def construct(self):
        q = Queue(scene=self)
        q.enqueue('a')
        q.enqueue('b')
        q.enqueue('c')
        q.enqueue('d')
        q.dequeue()
        q.dequeue()
        q.enqueue('e')
        q.enqueue('f')
        q.enqueue('g')
        q.enqueue('h')
        q.enqueue('i')
        q.dequeue()
        q.dequeue()
        q.dequeue()
        q.dequeue()
        q.dequeue()
        q.dequeue()

class BagExample(Scene):
    def construct(self):
        b = Bag(scene=self)
        b.put(1)
        b.put(2)
        b.put(3)
        b.put(4)
        b.put(5)
        b.pull()
        b.pull()
        b.pull()
        b.pull()

class FacadeScene(Scene):
    def construct(self):
        s = FacadeRA(scene=self,RAtype='stack')
        g = s.add('a')
        b = s.add('a')
        h = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
        c = s.add('a')
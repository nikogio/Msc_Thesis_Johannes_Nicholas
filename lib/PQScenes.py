from manim import *
from DataStructures.PriorityQueue import PriorityQueue

class PQScene(Scene):
     def construct(self):
          pq = PriorityQueue(scene=self)
          pq.insert(1)
          pq.insert(2)
          pq.insert(3)
          pq.insert(4)
          pq.insert(0)
          pq.delete_next()
          pq.delete_next()
          pq.delete_next()
          pq.delete_next()
          pq.delete_next()
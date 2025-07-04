from DataStructures.ResizingArray import ResizingArray
from manim import *

class PriorityQueue(ResizingArray):
    def __init__(self, scene:Scene, max_oriented:bool=False, side_length:float=2.0, size:int =2, **kwargs):
        super().__init__(scene = scene,**kwargs)
        self.max_oriented = max_oriented # Minimum oriented by default
        self.regular_add('-') # Always add '-' to occupy place 0.


    def insert(self,value):
        resized = False
        if self.is_full():
            self.scene.play(self.array.animate.to_edge(UP,buff=0.5))
            self.create_resized_array(doubling=True)
            self.copy_to_new_array()
            self.replace_old_array_with_new()
            self.regular_add(value)
            resized = True
        else:
            self.regular_add(value)
        
        self.swim(self.filled-1)
        return resized

    # Adds value to the last slot in the PQ
    def regular_add(self, value):
            self.scene.play(self.array.write(label=self.filled,value=value))
            self.filled+=1

    def delete_next(self):
        if not self.is_empty():
            if self.needs_decrease():
                self.scene.play(self.array.animate.to_edge(UP,buff=0.5))
                self.create_resized_array(doubling=False)
                self.copy_to_new_array()
                self.replace_old_array_with_new()
                self.scene.play(self.regular_delete())
            else:
                self.scene.play(self.regular_delete())

            self.sink(1)

    def regular_delete(self):
        self.filled -=1
        self.scene.play(AnimationGroup(
            Indicate(self.array.slots[1]),
            Indicate(self.array.slots[self.filled]),
            lag_rato=0
        ))
        self.scene.play(self.array.swap_values(1,self.filled))
        animation = self.array.delete(self.filled)
        return animation

    def swim(self,n):
         while self.needs_move_up(n):
            self.scene.play(AnimationGroup(
                            Indicate(self.array.slots[n]),
                            Indicate(self.array.slots[n//2]),
                            lag_ratio=0             
                            ))
            self.scene.play(self.array.swap_values(n,n//2))
            n = n//2

    def sink(self,n):
        while 2*n <= self.filled-1:

            j = 2*n

            if self.max_oriented:
                # Checking if we can sink to first or second child.
                if j < self.filled-1 and self.array.less(j,j+1):
                    j=j+1
                # Checking if we should sink and doing it.    
                if self.array.less(n,j):
                    self.scene.play(AnimationGroup(
                            Indicate(self.array.slots[n]),
                            Indicate(self.array.slots[j]),
                            lag_ratio=0             
                            ))
                    self.scene.play(self.array.swap_values(n,j))
                else:
                    break

            else:
                # Checking if we can sink to first or second child.
                if j < self.filled-1 and self.array.less(j+1,j):
                    j=j+1
                # Checking if we should sink and doing it.    
                if self.array.less(j,n):
                    self.scene.play(AnimationGroup(
                            Indicate(self.array.slots[n]),
                            Indicate(self.array.slots[j]),
                            lag_ratio=0             
                            ))
                    self.scene.play(self.array.swap_values(n,j))
                else:
                    break
            n = j

    def needs_move_up(self, slot:int):
         if slot>1:
            if self.max_oriented:
                if self.array.get_value(slot) > self.array.get_value(slot//2):
                    return True  
            else:
                if self.array.get_value(slot) < self.array.get_value(slot//2):
                    return True
         else:
              return False
    
    def is_empty(self):
        if self.filled ==1: # First slot is always "empty."
            return True
        else:
            return False
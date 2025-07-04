# DESCRIPTION

from manim import *
from DataStructures.Array import Array
from DataStructures.Array import Slot
from DataStructures.ArrayFactory import ArrayFactory
import random

class ResizingArray(VMobject):
    def __init__(self,scene:Scene, side_length:float=2.0,size:int=1,
                 center:np.array=[0,0,0], # The default center of the arrays
                 left_edge:np.array=[-7,0,0], # The default left_edge of the arrays
                                                # Arrays exceeding the space from left to right will resize to fit.
                 screen_rectangle: Rectangle = Rectangle(height=7.9,width=13.9), # Default is full screen.
                 **kwargs):
        super().__init__(**kwargs)
        self.screen_rectangle = screen_rectangle
        self.factory = ArrayFactory(screen_rectangle)
        self.left_edge=left_edge
        self.object_center=center,
        self.array = self.factory.create_initial_array(size=size,
                                                        side_length=side_length)
        self.filled = 0
        self.scene = scene
        self.add(self.array)
        self.scene.play(Create(self.array))

            
    def instantiate_resized_array(self,doubling:bool):
        self.new_array = self.factory.create_array(size=self.array.size, ini_array=self.array, doubling=doubling)
        self.new_array_temporary =self.new_array.copy()
        self.new_array_temporary.move_to(self.screen_rectangle.get_bottom()).shift(UP*self.new_array_temporary.height/2)


    def create_new_array_on_screen(self):
        self.scene.play(Create(self.new_array_temporary))
    
    def move_old_array_into_place_for_replacement(self):
        copy_old_array = self.array.copy()
        copy_old_array.move_to(self.screen_rectangle.get_top()).shift(copy_old_array.height/2*DOWN)
        initial_height_old_array = copy_old_array.height
        while copy_old_array.get_bottom()[1]-0.08<self.new_array_temporary.get_top()[1] and copy_old_array.height>=initial_height_old_array/1.5:
            # Below are two options for how to fit old + new array.
            # Scaling (Shrinking both vert. + hori.) or Stretching (Shirnking only vert.)
            #copy_old_array.stretch(0.98,1)
            copy_old_array.scale(0.98)
            copy_old_array.move_to(self.screen_rectangle.get_top()).shift(copy_old_array.height/2*DOWN)
            #self.new_array_temporary.stretch(0.98,1)
            self.new_array_temporary.scale(0.98)
            self.new_array_temporary.move_to(self.screen_rectangle.get_bottom()).shift(UP*self.new_array_temporary.height/2)
        self.scene.play(Transform(self.array,copy_old_array))



    def copy_to_new_array(self):
        for i in range(self.array.size):
            if self.array.has_value(i):
                original_slot_copy = self.array.create_slot_copy(i) # Copy of slot in original array
                new_slot_copy = self.new_array_temporary.create_slot_copy(i,new_value=self.array.slots[i].get_value())
                # Below adds indication pr. slot before copying. (We may or may not want it).
                self.indicate_slot(self.array.slots[i])
                self.scene.add(original_slot_copy) # Adding copy to the scene.
                # End of Indication animation.
                self.scene.play(AnimationGroup(
                    original_slot_copy.animate.move_to(self.new_array_temporary.slots[i].get_center()),
                    Transform(original_slot_copy,new_slot_copy)
                ))
                self.new_array.slots[i].set_value(self.array.slots[i].get_value()) # Setting of the actual array
                self.new_array_temporary.slots[i].set_value(self.array.slots[i].get_value()) # Setting of the temp array
                self.scene.remove(original_slot_copy)


    def replace_old_array_with_new(self):
        old_array = self.array
        self.array = self.new_array
        self.array.move_to(self.screen_rectangle.get_center()) # Should already be there
        self.scene.play(FadeOut(old_array))
        self.scene.play(Transform(self.new_array_temporary,self.array))
        self.scene.add(self.new_array)
        self.scene.remove(self.new_array_temporary)

    def is_full(self):
        if self.filled==self.array.size:
            return True
        else:
            return False
        
    def needs_decrease(self):
        if self.filled<=0.25*self.array.size:
            return True
        else:
            return False
        
    def indicate_slot(self,slot:Slot):
        copy = self.copy_slot_for_indicate(slot)
        self.scene.remove(slot)
        self.scene.play(Indicate(copy))
        self.scene.add(slot)
        self.scene.remove(copy)

    def copy_slot_for_indicate(self,slot:Slot):
        original_slot = slot
        copy_square = Square(side_length=original_slot.square.height).move_to(original_slot.square)
        copy_text = original_slot.value_text.copy()
        copy_label = original_slot.label_text.copy()
        copy_vgroup = VGroup(copy_square,copy_text,copy_label)
        return copy_vgroup

class Stack(ResizingArray):
    #Constructor method
    def __init__(self, scene:Scene, side_length:float=2.0, size:int =1,
                                  screen_rectangle: Rectangle = Rectangle(height=7.9,width=13.9), # Default is full screen.
                                  **kwargs):
        super().__init__(scene = scene,screen_rectangle=screen_rectangle,**kwargs)

    def push(self,value):
        resized = False
        if self.is_full():
            self.instantiate_resized_array(doubling=True)
            self.move_old_array_into_place_for_replacement()
            self.create_new_array_on_screen()
            self.copy_to_new_array()
            self.replace_old_array_with_new()
            self.regular_push(value)
            resized = True
        else:
            self.regular_push(value)
        return resized

    def regular_push(self, value):
            self.scene.play(self.array.write(label=self.filled,value=value))
            self.filled+=1

    def pop(self):
        if self.needs_decrease():
            self.instantiate_resized_array(doubling=False)
            self.move_old_array_into_place_for_replacement()
            self.create_new_array_on_screen()
            self.copy_to_new_array()
            self.replace_old_array_with_new()
            self.scene.play(self.regular_pop())
        else:
            self.scene.play(self.regular_pop())

    def regular_pop(self):
        self.filled -=1
        animation = self.array.delete(self.filled)
        return animation


class Queue(ResizingArray):
    #Constructor method
    def __init__(self, scene:Scene, side_length:float=2.0, size:int =1,
                screen_rectangle: Rectangle = Rectangle(height=7.9,width=13.9), # Default is full screen
                **kwargs):
        super().__init__(scene = scene,screen_rectangle=screen_rectangle,**kwargs)
        self.next = 0 # Next to leave the queue
        self.last = None # Last in the queue

    def enqueue(self,value):
        resized = False
        if self.is_full():
            self.instantiate_resized_array(doubling=True)
            self.move_old_array_into_place_for_replacement()
            self.create_new_array_on_screen()
            self.copy_to_new_array()
            self.replace_old_array_with_new()
            self.regular_enqueue(value)
            resized = True
        else:
            self.regular_enqueue(value)
        return resized

    def regular_enqueue(self, value):
            if self.filled==0:
                self.last = 0
            #Increment self.last OR move it back to label 0.
            elif self.last==self.array.size-1: # last is currently at the last slot of the array.
                self.last=0
            else: # the last slot is available
                self.last+=1
            #Write the value.
            self.scene.play(self.array.write(label=self.last,value=value))
            self.filled+=1

    def dequeue(self):
        resized = False
        if self.needs_decrease():
            self.instantiate_resized_array(doubling=False)
            self.move_old_array_into_place_for_replacement()
            self.create_new_array_on_screen()
            self.copy_to_new_array()
            self.replace_old_array_with_new()
            self.scene.play(self.regular_dequeue())
            resized = True
        else:
            self.scene.play(self.regular_dequeue())
        return resized

    def regular_dequeue(self):
        animation = self.array.delete(self.next)
        if self.next == self.array.size:
            self.next=0
        else:
            self.next+=1
        self.filled -=1
        return animation
    
    #OVERRIDDEN from parent class.
    def copy_to_new_array(self):
        new_array_next=0
        for i in range(self.next,self.array.size):
            if self.array.has_value(i):
                original_slot_copy = self.array.create_slot_copy(i) # Copy of slot in original array
                new_slot_copy = self.new_array_temporary.create_slot_copy(new_array_next,new_value=self.array.slots[i].get_value())
                # Below adds indication pr. slot before copying. (We may or may not want it).
                self.indicate_slot(self.array.slots[i])
                self.scene.add(original_slot_copy) # Adding copy to the scene.
                # End of Indication animation
                self.scene.play(AnimationGroup(
                    original_slot_copy.animate.move_to(self.new_array_temporary.slots[new_array_next].get_center()),
                    Transform(original_slot_copy,new_slot_copy)
                ))
                self.new_array.slots[new_array_next].set_value(self.array.slots[i].get_value())
                self.new_array_temporary.slots[new_array_next].set_value(self.array.slots[i].get_value())
                self.scene.remove(original_slot_copy)
            new_array_next+=1

        for i in range(0,self.next):
            if self.array.has_value(i):
                original_slot_copy = self.array.create_slot_copy(i) # Copy of slot in original array
                new_slot_copy = self.new_array_temporary.create_slot_copy(new_array_next,new_value=self.array.slots[i].get_value())
                # Below adds indication pr. slot before copying. (We may or may not want it).
                self.indicate_slot(self.array.slots[i])
                self.scene.add(original_slot_copy) # Adding copy to the scene.
                # End of Indication animation
                self.scene.play(AnimationGroup(
                    original_slot_copy.animate.move_to(self.new_array_temporary.slots[new_array_next].get_center()),
                    Transform(original_slot_copy,new_slot_copy)
                ))
                self.new_array.slots[new_array_next].set_value(self.array.slots[i].get_value())
                self.new_array_temporary.slots[new_array_next].set_value(self.array.slots[i].get_value()) # Setting of the actual array
                self.scene.remove(original_slot_copy)
            new_array_next+=1
        #Setup for new array.
        self.next = 0
        self.last = self.array.size-1

class Bag(ResizingArray):
    #Constructor method
    def __init__(self, scene:Scene, side_length:float=2.0, size:int =1, seed:int=1,
                    screen_rectangle: Rectangle = Rectangle(height=7.9,width=13.9), # Default is full screen.
                    **kwargs):
        super().__init__(scene = scene,screen_rectangle=screen_rectangle,**kwargs)
        self.occupied = set()
        self.available = set()
        random.seed(seed)
        for i in range(size):
            self.available.add(i)

    def put(self, value):
        resized = False
        if self.is_full():
            self.instantiate_resized_array(doubling=True)
            self.move_old_array_into_place_for_replacement()
            self.create_new_array_on_screen()
            self.copy_to_new_array()
            for i in range (self.array.size,2*self.array.size):
                self.available.add(i)
            self.replace_old_array_with_new()
            self.regular_put(value)
            resized = True
        else:
            self.regular_put(value)
        return resized

    def regular_put(self, value):
        placement = random.choice(tuple(self.available))
        self.available.remove(placement)
        self.occupied.add(placement)
        self.scene.play(self.array.write(label=placement,value=value))
        self.filled+=1

    def pull(self):
        resized=False
        if self.needs_decrease():
            self.instantiate_resized_array(doubling=False)
            self.move_old_array_into_place_for_replacement()
            self.create_new_array_on_screen()
            self.copy_to_new_array()
            self.replace_old_array_with_new()
            self.scene.play(self.regular_pull())
            self.available.clear()
            self.occupied.clear()
            for i in range(self.array.size):
                if self.array.has_value(i):
                    self.occupied.add(i)
                else:
                    self.available.add(i)
            resized=True
        else:
            self.scene.play(self.regular_pull())
        return resized

    def regular_pull(self):
        placement = random.choice(tuple(self.occupied))
        self.available.add(placement)
        self.occupied.remove(placement)
        self.filled -=1
        animation = self.array.delete(placement)
        return animation
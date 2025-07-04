from manim import *
from DataStructures.Array import Array
from DataStructures.Memory import Memory

#this scene renders a Memory oject animaton, done with the Array class which subclass is Slot
class MemorySlideMerged(Scene):
    def construct(self):
    # Create a MemoryArray object
        array = Array(size=45, side_length=1, memory=True)
        screen_rect = FullScreenRectangle()
        array.arrange_on_screen(screen_rect)
        self.add(array)
        array.add_legend("Occupied", "Reserved", "Available")
      
        # Select a random slot to be occupied
        slot = array.access_random()
        #and pick another random for reserved
        slot2=array.access_second_random(slot)
        #first method
        self.wait()
        slot_copy = slot.copy()
        slot2_copy = slot2.copy()
        #second method 
        slot2_copy.move_to(slot2.get_center())
        
        #slot_copy.set_color(RED)
        self.play(slot_copy.animate.set_color(RED))
        self.add(slot2_copy)
        self.play(AnimationGroup(Indicate(slot2_copy, scale_factor=1.2,color=BLUE)),
                            slot2.animate.set_color(BLUE))
        self.wait(2)
        self.remove(slot2_copy)
        # Animate the movement of the slot copy to the center of the MemorySlot object at index 3
        slot_copy.move_to(slot2.get_center())
        # Change the color of the MemorySlot object at index 0 to green
        self.play(slot.animate.set_color(GREEN),slot2.animate.set_color(RED))
        # Change the color of the MemorySlot object at index 3 back to red
        
        self.play(slot2.animate.set_fill(opacity=0)) 
        self.play(slot.animate.set_fill(opacity=0))
        
        
class MemoryHT(Scene):
    #old memory scene
    def construct(self):
    # Create a MemoryArray object
        array = Array(size=45, side_length=1, memory=True)
        screen_rect = Rectangle(height=4,width=14).move_to([0,-2,0])
        
        #get height of fullscreen, halve it and place 
        array.arrange_on_screen(screen_rect)
        self.add(array)
        array.add_legend("Occupied", "Reserved", "Available")
      
        # Select a random slot to be occupied
        slot = array.access_random()
        #and pick another random for reserved
        slot2=array.access_second_random(slot)
        self.wait()
        slot_copy = slot.copy()
        slot2_copy = slot2.copy()
        slot2_copy.move_to(slot2.get_center())
        
        #slot_copy.set_color(RED)
        self.play(slot_copy.animate.set_color(RED))
        self.add(slot2_copy)#
        self.play(AnimationGroup(Indicate(slot2_copy, scale_factor=1.2,color=BLUE)),
                            slot2.animate.set_color(BLUE))
        self.wait(2)
        self.remove(slot2_copy)#
        # Animate the movement of the slot copy to the center of the MemorySlot object at index 3
        slot_copy.move_to(slot2.get_center())
        # Change the color of the MemorySlot object at index 0 to green
        self.play(slot.animate.set_color(GREEN),slot2.animate.set_color(RED) )
        # Change the color of the MemorySlot object at index 3 back to red
        
        self.play(slot2.animate.set_fill(opacity=0)) 
        self.play(slot.animate.set_fill(opacity=0))

class MemoryScene(Scene):
    def construct(self):
        r = Rectangle(height=4,width=14).move_to([0,0,0])
        m = Memory(screen_rect=r,scene=self)
        i = m.add_value()
        j = m.add_value()
        k = m.add_value()
        m.remove_value(i)
        m.remove_value(j)
        m.remove_value(k)
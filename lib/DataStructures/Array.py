from manim import *
from DataStructures.Slot import Slot

class Array(VMobject):
    def __init__(self,hash_table:bool=False,
                 size:int =1, side_length:float=2.0,
                 color_coding:bool=False,
                 **kwargs):
        super().__init__(**kwargs)
        if hash_table:
            self.slots = VGroup(*[Slot(hash_table=True, side_length=side_length, label=i,color_coding=color_coding)for i in range(size)])
            self.slots.arrange(DOWN,buff=0)
        else:
            self.slots = VGroup(*[Slot(side_length=side_length, label=i,color_coding=color_coding) for i in range(size)])
            self.slots.arrange(buff=0)
        self.add(self.slots)
        self.color_coding=color_coding
        self.size=size

    def create_array(self):
        return Write(self)

    def delete_array(self):
        return FadeOut(self)
    
    def get_side_lenght(self):
        return self.slots[0].get_side_length()
    
    # UNUSED METHOD 
    def memory_swap(self,first,second):
        # takes two random slot and scene, one is busy, other is prepared
        # swap changing colour, the new one is red, old one is first green
        # then blank
        #first_copy = self.create_slot_copy(first.slots.)
        first_copy = self.copy()   
        #substitute with copy
        second_copy = self.copy()
        second_copy.move_to(second.get_center())
        first_copy.set_color(RED)
        self.scene.add(second_copy)
        second.set_color(BLUE)
        self.scene.play(Indicate(second_copy, scale_factor=1.2,color=BLUE))
        self.scene.remove(second_copy)
        first_copy.move_to(second.get_center())
        first.set_color(GREEN)
        second.set_color(RED)
        second.set_fill(opacity=0)
        first.set_fill(opacity=0)
    
    def write(self, label:int, value):
        return self.slots[label].set_value(value)
    
    def read(self, label:int):
        return Indicate(self.slots[label])
    
    def get_value(self, label:int):
        return self.slots[label].get_value()
    
    def delete(self, label:int):
        return self.slots[label].remove_value()
    
    def has_value(self,label:int):
        if self.get_value(label) == None:
            return False
        else:
            return True
        
    def swap_values(self, this, that):
        # Setup
        this_text = self.slots[this].value_text
        that_text = self.slots[that].value_text
        this_value = self.slots[this].value
        that_value = self.slots[that].value
        # Change Text Mobjects (As SubMobjects of Slots)
        self.slots[this].remove(this_text)
        self.slots[that].remove(that_text)
        self.slots[this].add(that_text)
        self.slots[that].add(this_text)
        # Change Text objects (Only the reference)
        self.slots[this].value_text = that_text
        self.slots[that].value_text = this_text
        # Change underlying values
        self.slots[this].value = that_value
        self.slots[that].value = this_value
        #self.slots[that].value = this_value
        # Change references to the slots in the VGroup
        return CyclicReplace(this_text,that_text)

    # Is this less than that?
    def less(self, this:int, that:int):
        this_value = self.get_value(this)
        that_value = self.get_value(that)

        if this_value is None and that_value is None:
            return False
        if this_value is None and that_value is not None:
            return True
        if this_value is not None and that_value is None:
            return False
        
        if type(this_value)!=type(that_value):
            raise ValueError("This and that value are not of the same type.")
        
        if this_value < that_value:
            return True
        else:
            return False
        
    # Creates an exact copy of a Slot in the same place of the Slot.
    # To be used in the copy_to_new_array method in ResizingArray.py
    def create_slot_copy(self,i:Integer,new_value=False):
        original_slot = self.slots[i]
        slot_copy = original_slot.copy()
        slot_copy.move_to(original_slot.get_center())
        slot_copy.remove_label()
        if new_value:
            slot_copy.set_value(new_value)
        return slot_copy
    


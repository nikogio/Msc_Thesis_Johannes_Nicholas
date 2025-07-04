import numbers
from manim import *

class Slot(VMobject):
    def __init__(self,value=None, side_length: float = 2.0,
                 hash_table:bool=False,label: int =0,
                 color_coding:bool=False,
                 **kwargs):
        super().__init__(**kwargs)
        self.square = Square(side_length=side_length).set_fill(BLACK)
        self.add(self.square)
        self.value=None
        self.value_text=None
        self.color_coding =color_coding
        if value:
                self.set_value(value)
        self.label=None
        self.set_label(label,hash_table)
        self.state = 0 # For Memory. (Available = 0, Occupied = 1, Reserved = 2)


    # This method should only takes strings and ints.
    # ints above 3 digits and strings above 1 character are turned into ###
    def set_value(self, value):
        if self.value:
            self.remove(self.value)        
        text = Text(str(value)).move_to(self.square).scale(self.square.height).set_z_index(1)
        self.value=value
        self.value_text=text # Setting the Text as a field of the Slot, so it can be retrieved later.
        self.add(text) # Adding the Text to the Slot.
        return AnimationGroup(Write(text))
    
    def set_color(self,color,opacity:int=2.0):
        self.square.set_fill(color=color, opacity=opacity)

    def get_value(self):
        return self.value
    
    def get_side_length(self):
        return self.square.side_length
    
    def get_label(self):
        return self.label
    
    def remove_value(self):
        if self.value!=None:
            to_remove = self.value_text
            self.remove(self.value_text)
            self.value=None
            return FadeOut(to_remove)
        
    def scale_slot_to_height(self,new_height):
        while self.height>new_height:
            self.scale(0.95)
    
    def set_label(self, label:int,hash_table:bool=False):
        label_text = self.generate_label_text(label)
        label_text.scale(0.35*self.square.height).next_to(self,DOWN,buff=0.25*self.square.height)
        if hash_table:
            label_text.next_to(self,LEFT,buff=0.12*self.square.height)
        self.label = label_text # Setting the Text as a field of the Slot, so it can be retrieved later
        self.label_text=label_text
        self.add(label_text)# Adding the Text to the slot.

    def remove_label(self):
        self.remove(self.label)

    def label_to_dots(self,hash_table:bool=False):
        if self.label is not None:
            self.remove_label()
        label_text = Text("...")
        label_text.scale(0.35*self.square.height).next_to(self,DOWN,buff=0.25*self.square.height)
        if hash_table:
            label_text.next_to(self,LEFT,buff=0.12*self.square.height)
        self.label = label_text # Setting the Text as a field of the Slot, so it can be retrieved later
        self.add(label_text)# Adding the Text to the slot.

    def generate_label_text(self,label: int):
        label_str = str(label)
        # if len(label_str)>3: #If label is 3 < digits, make it '###'
        #     label_str='###'
        label_str = '['+label_str+']'
        text = Text(label_str)
        return text
    
    def generate_text(self,value):
        #If value is an int, only allow 2 digits.
        if isinstance(value, numbers.Number) and int(value)==value:
            value_string = str(value)
            if len(value_string)>3:
                value_string='###'
        #If value is a string, only allow 1 character.
        elif isinstance(value,str):
            value_string = value
            if len(value)>1:
                value_string='###'
        else:
            raise ValueError("Error: Values in Slots can only be strings or integers.")
        text = Text(value_string)
        return text
    
    def set_state(self,state,color=None):
        if not self.color_coding:
            if state==0: # Available
                self.set_color(color=BLACK,opacity=0)
                self.state=0
            elif state == 1: # Occupied
                self.set_color(RED,opacity=1)
                self.state=1
            elif state == 2: # Reserved
                self.set_color(BLUE,opacity=1)
                self.state=2
        else:
            if state == 0: # Available
                self.set_color(color=BLACK,opacity=1)
                self.state=state
            else:
                self.set_color(color=color,opacity=1)
                self.state=state
            if color!=None:
                self.set_color(color=color,opacity=1)
                self.state=state

    def set_slot_color(self,color):
        self.set_color(color,opacity=1)

    def return_to_state_color(self):
        if self.state==0: # Available
            self.set_color(color=BLACK,opacity=0)
        elif self.state == 1: # Occupied
            self.set_color(RED,opacity=1)
        elif self.state == 2: # Reserved
            self.set_color(BLUE,opacity=1)
            
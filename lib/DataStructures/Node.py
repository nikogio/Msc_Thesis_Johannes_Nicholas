import numbers
from manim import *

class Node(VMobject):
    def __init__(self,value=None, radius: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=radius,color=WHITE)
        self.add(self.circle)
        self.value = value
        self.value_text=None
        self.set_value(value)


    # This method should only takes strings and ints.
    # ints above 3 digits and strings above 1 character are turned into ###
    def set_value(self, value): 
        text = self.generate_text(value)      
        text.move_to(self.circle).scale(self.circle.radius*2).set_z_index(1)
        self.value_text=text # Setting the Text as a field of the Node, so it can be retrieved later.
        self.add(text) # Adding the Text to the Node.
    
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
    
    def get_value(self):
        return self.value
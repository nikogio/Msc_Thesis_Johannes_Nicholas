from manim import *
from DataStructures.Array import Array

class ArrayFactory:
    def __init__(self,
                 screen_rectangle:Rectangle=Rectangle(height=8,width=14) # The rectangle the arrays must fit in
                 ):
        self.array = None
        self.screen_rectangle = screen_rectangle

    def create_array(self,
                     size,
                     ini_array,
                     doubling:bool,
                     hash_table:bool=False):
        if doubling:
            size *= 2
            self.array = Array(size=size, side_length=ini_array.get_side_lenght()*0.95,hash_table=hash_table)
        else:
            self.array = Array(size=int(0.5*size), side_length=ini_array.get_side_lenght()*1.05,hash_table=hash_table)
        #Aligning the array
        self.array.move_to(self.screen_rectangle.get_center())

        #Correcting if size is to big.
        self.check_and_adjust_array_horizontal_size(
                                         current_size=size,
                                         current_side_length=self.array.slots[0].square.side_length,
                                         hash_table=hash_table)
        self.check_and_adjust_array_vertical_size(current_size=size,
                                                  current_side_length=self.array.slots[0].square.side_length,
                                                  hash_table=hash_table)
        
        return self.array
    
    def create_initial_array(self,size,side_length,
                             hash_table:bool=False):
        self.array = Array(size=size,
                           side_length=side_length,
                           hash_table=hash_table).move_to(self.screen_rectangle.get_center())
        self.side_length = side_length
        self.check_and_adjust_array_horizontal_size(current_size=size,
                                                    current_side_length=side_length,
                                                    hash_table=hash_table)
        self.check_and_adjust_array_vertical_size(current_size=size,
                                                  current_side_length=side_length,
                                                  hash_table=hash_table)

        return self.array

    def check_and_adjust_array_horizontal_size(self, current_size,
                                               current_side_length,
                                               hash_table:bool=False):
        left = self.array.slots.get_left()
        while (left[0])<(self.screen_rectangle.get_left()[0]):
            current_side_length*=0.95
            self.array=Array(size=current_size,
                             side_length=current_side_length,
                             hash_table=hash_table).move_to(self.screen_rectangle.get_center())
            left=self.array.slots.get_left()

    def check_and_adjust_array_vertical_size(self, current_size,
                                             current_side_length,
                                             hash_table:bool=False):
        bottom = self.array.slots.get_bottom()
        while (bottom[1])<(self.screen_rectangle.get_bottom()[1]):
            current_side_length*=0.95
            self.array=Array(size=current_size,
                             side_length=current_side_length,
                             hash_table=hash_table).move_to(self.screen_rectangle.get_center())
            bottom=self.array.slots.get_bottom()
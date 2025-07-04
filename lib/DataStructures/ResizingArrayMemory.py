from manim import *
from DataStructures.ResizingArray import ResizingArray, Stack, Queue, Bag
from DataStructures.PriorityQueue import PriorityQueue
from DataStructures.Memory import Memory
from DataStructures.FacadeResizingArray import FacadeRA

class RAMemory(VMobject):
    def __init__(self,
                 scene:Scene,
                 RAtype:str,
                 side_length:int=2,
                 size:int = 1, # Starting size of the RA array.
                 nr_of_lines:int=4,
                 slots_pr_line:int=20,
                 max_oriented:bool=False, #Only relevant for PQ
                 ):
        # Scene setup
        self.upper_R= Rectangle(height=4,width=14).move_to([0,1.9,0])
        self.lower_R= Rectangle(height=3,width=14).move_to([0,-2.5,0])
        self.scene=scene
        # Setup of underlying data structure.
        self.facade = FacadeRA(RAtype,side_length = side_length, scene = self.scene,
                                screen_rectangle= self.upper_R, max_oriented = max_oriented)

        #Setting up Memory
        self.memory = Memory(screen_rect = self.lower_R,
                        slots_pr_line=slots_pr_line,
                        nr_of_lines=nr_of_lines,
                        scene=self.scene)
        self.ht_array = self.memory.select_random_slots(size) # The slots where the HT array is located.
        self.next_empty_slot=None
        if self.facade.RAtype in ['stack','queue','bag']:
            self.memory.set_multiple_slot_state(self.ht_array,2)
            self.next_empty_slot = self.ht_array[0]
        else:
            self.memory.set_slot_state(self.ht_array[0],1)
            self.memory.set_multiple_slot_state(self.ht_array[1:],2)
            self.next_empty_slot = self.ht_array[1]


    def add(self,value):
        resized = self.facade.add(value)
        if resized:
            if len(self.ht_array)*2> self.memory.slots_pr_line:
                raise RuntimeError("You don't have enough slots per line in Memory to continue growing the array.")
            new_ht_array = self.memory.select_random_slots(len(self.ht_array)*2)
            self.memory.set_multiple_slot_state(new_ht_array,2)
            self.memory.set_multiple_slot_state(new_ht_array[:len(new_ht_array)//2],1)
            self.memory.set_slot_state(new_ht_array[int(len(new_ht_array)/2)],1)
            self.memory.set_multiple_slot_state(self.ht_array,0)
            self.ht_array = new_ht_array
            if len(new_ht_array)!=2: # Edge case
                self.next_empty_slot = new_ht_array[int(len(new_ht_array)/2)+1]
        else:
            self.memory.set_slot_state(self.next_empty_slot,1)
            self.next_empty_slot+=1

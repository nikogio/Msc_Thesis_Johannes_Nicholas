from manim import *
from DataStructures.Array import Array
import random

class Memory(Array):
    def __init__(self,
                 screen_rect: Rectangle=None,
                 slots_pr_line:int=20,
                 nr_of_lines:int = 4,
                 scene: Scene = None,
                 color_coding:bool=False,
                 **kwargs):
        self.size = slots_pr_line * nr_of_lines + (2 * nr_of_lines) # results in usable amount of slots
                                                                     # being lines * slots pr line.
        super().__init__(size = self.size,color_coding=color_coding,**kwargs)
        self.scene=scene
        self.color_coding=color_coding
        self.screen_rect = screen_rect
        self.slots_pr_line = slots_pr_line
        self.nr_of_lines = nr_of_lines
        self.arrange_on_screen()
        self.scene.play(Create(self.slots))
        

        

    def arrange_on_screen(self):
        #lines are lists of vgrouped slots of x slots
        lines = [VGroup(*self.slots[i:i+self.slots_pr_line+2]) for i in range(0, self.size, self.slots_pr_line+2)]
        # Move top line into place
        self.move_lines_into_place(lines)         
        # Stretching down size if it is too large.
        self.stretch_to_fit(lines,1)
        self.stretch_to_fit(lines,0)
        self.setup_labels_memory(lines)

    # Helper method for arrange_on_screen().
    def move_lines_into_place(self, lines):
            lines[0].move_to(self.screen_rect.get_top()).shift((self.slots[0].height/2)*DOWN)
            for i in range(1, len(lines)):
                lines[i].next_to(lines[i-1], DOWN, buff=self.slots[i].height/4)

    # Helper method for arrange_on_screen().
    # dir = 1 is vertical. dir = 0 is horizontal.
    def stretch_to_fit(self, lines, dir):
        if dir == 1:
            while lines[len(lines)-1].get_bottom()[1]<self.screen_rect.get_bottom()[1]:
                for line in lines:
                    line.stretch(0.98,dir)
                self.move_lines_into_place(lines)

        elif dir ==0:
            while lines[0].get_left()[0]+(self.slots[0].square.width*0.65) < self.screen_rect.get_left()[0]:
                for line in lines:
                    line.stretch(0.98,dir)
                self.move_lines_into_place(lines)
        else:
            raise ValueError("dir in stretch_to_fit() must be 0 or 1")
        

    def setup_labels_memory(self,
                            lines):
        self.remove_labels(lines)
        self.create_labels_memory(lines)
        self.edge_labels_to_dots()

    def remove_labels(self,lines):
        #remove labels to avoid having them stretched
        for line in lines:
            for slot in line:
            # self.slots[i]
                slot.remove(slot.label)

    def create_labels_memory(self,lines):
        #iterate through each slot of the lines, increment randomly
        n = random.randint(1,300)
        for i in range(len(lines)):
            for slot in lines[i]:
                slot.set_label(n)
                n+=1
            n+=random.randint(1,300)

    def edge_labels_to_dots(self):
        self.find_edge_slots()
        for i in self.edge_slots:
            self.slots[i].label_to_dots(hash_table=False)

    def find_edge_slots(self):
        self.edge_slots =[]
        for i in range(0, self.size, self.slots_pr_line+2):
            self.edge_slots.append(i) # Left side
            self.edge_slots.append(i+self.slots_pr_line-1+2) # Right side


    # WARNING: THIS METHOD CAN LEAD TO AN INFINITE WHILE LOOP      
    def select_random_slots(self,n):
        while True:
            first = self.access_random_slot()
            continue_while_loop = False
    
            for i in range(first + 1, first + n):
                if not self.slot_is_eligible(i):
                    continue_while_loop = True
                    break
    
            if continue_while_loop:
                continue
    
            # Continue with the rest of your code here if the for loop completes without a break
            break

        slots_to_return = []
        for i in range(first,first+n):
            slots_to_return.append(i)
        return slots_to_return
    
    # WARNING: THIS METHOD CAN LEAD TO AN INFINITE WHILE LOOP      
    def select_random_slots(self,n):
        while True:
            first = self.access_random_slot()
            continue_while_loop = False
    
            for i in range(first + 1, first + n):
                if not self.slot_is_eligible(i):
                    continue_while_loop = True
                    break
    
            if continue_while_loop:
                continue
    
            # Continue with the rest of your code here if the for loop completes without a break
            break

        slots_to_return = []
        for i in range(first,first+n):
            slots_to_return.append(i)
        return slots_to_return
        
    def access_random_slot(self):
        i=0
        while True:
            i = random.randint(0,len(self.slots)-1)
            if self.slot_is_eligible(i):
                break
        return i
    
    def slot_is_eligible(self,i):
        to_return = True
        if i in self.edge_slots:
            to_return = False
        if self.slots[i].state == 1 or self.slots[i].state==2:
            to_return = False
        return to_return
    
    def set_slot_state(self,i,state,color=None):
        slot_copy = self.create_slot_copy(i)
        slot_copy.set_z_index(1) # Move copy in front original
        slot_copy.set_state(self.slots[i].state)
        slot_copy.square.set_fill(opacity=1)
        self.scene.add(slot_copy)
        if state == 0:
            self.slots[i].set_state(state,BLACK)
        else:
            self.slots[i].set_state(state,color)
        self.scene.play(FadeOut(slot_copy))

    def set_multiple_slot_state(self,i_array,state,colorarray=None):
        slot_copies = [self.create_slot_copy(i) for i in i_array]
        slot_copies_vgroup = VGroup()
        for i in range(len(i_array)):
            slot_copies[i].set_z_index(1)
            slot_copies[i].set_state(self.slots[i_array[i]].state)
            slot_copies[i].square.set_fill(opacity=1)
            slot_copies_vgroup.add(slot_copies[i])
        self.scene.add(slot_copies_vgroup)
        for i in range(len(i_array)):
            if self.color_coding:
                if state == 0:
                    self.slots[i_array[i]].set_state(state,BLACK)
                else:
                    self.slots[i_array[i]].set_state(state,colorarray[i])
            else:
                self.slots[i_array[i]].set_state(state)
        
        self.scene.play(FadeOut(slot_copies_vgroup))

    # Intentionally does not produce an animaton such as FadeOut.
    def set_slot_color(self,i,color):
        self.slots[i].set_slot_color(color)

    def set_multiple_slot_color(self,i_array,color):
        for i in i_array:
            self.slots[i].set_slot_color(color)

    def return_slot_to_state_color(self,i):
        self.slots[i].return_to_state_color()

    def return_multiple_slot_to_state_color(self,i_array):
        for i in i_array:
            self.slots[i].return_to_state_color()

    def add_value(self):
        i = self.access_random_slot()
        self.set_slot_state(i,1)
        return i 

    
    def remove_value(self,i):
        self.set_slot_state(i,0)




# Unused at the moment
    def add_legend(self, busy, reserved, available):
        occ_slot = Square(side_length=0.4, fill_color=RED, fill_opacity=1).set_stroke(width=1.5)
        res_slot = Square(side_length=0.4, fill_color=BLUE, fill_opacity=1).set_stroke(width=1.5)
        av_slot = Square(side_length=0.4, fill_color=GREEN_C, fill_opacity=1).set_stroke(width=1.5)
        legend = VGroup(
            occ_slot,
            Text(busy, font_size=18).next_to(occ_slot, RIGHT),
            res_slot.next_to(occ_slot, RIGHT),
            Text(reserved, font_size=18).next_to(res_slot, RIGHT),
            av_slot.next_to(res_slot, RIGHT),
            Text(available, font_size=18).next_to(av_slot, RIGHT),
        ).arrange(RIGHT, buff=0.25).to_corner(DR)
        self.add(legend)
from manim import *
from DataStructures.Array import Array

class SwapScene(Scene):
    def construct(self):
        array = Array(size=4)
        array.write(label=0,value=0)
        array.write(label=1,value=1)
        array.write(label=2,value=2)
        array.write(label=3,value=3)
        self.play(Create(array))
        self.play(array.swap_values(1,3))
        self.play(array.swap_values(0,3))
        self.play(Indicate(array.slots[3]))
        
class ArraySceneHashTable(Scene):
    def construct(self):
        array = Array(size=4,hash_table=True)
        self.play(Create(array))
        self.wait()
        self.play(array.write(label=0,value='a'))
        self.play(array.read(label=0))
        self.wait()
        self.play(array.delete(0))
        
class ArraySceneMemory(Scene):
    def construct(self):
        slots_p_line = 10
        lines=3
        amount = slots_p_line*lines
        r = Rectangle(width=14,height=4).move_to([0,-2,0])
        array = Array(size=amount)
        array.arrange_on_screen(r,slots_p_line)
        #self.add(r)
        self.play(Create(array))
        self.wait()
        
class ArraySceneMemoryMovement(Scene):
    def construct(self):
        slots_p_line = 20
        lines=4
        amount = slots_p_line*lines
        r = Rectangle(width=14,height=4).move_to([0,-2,0])
        array = Array(size=amount,scene=self,memory=True,screen_rect=r,
                      slots_pr_line=slots_p_line,
                      nr_of_lines=lines)
        #self.add(r)
        self.wait()
        slots = array.select_random_slots(4)
        array.set_multiple_slot_state(slots,state=1)
        self.wait(1)
        i = array.access_random_slot()
        array.set_slot_state(i,1)
        self.wait()
        i = array.access_random_slot()
        array.set_slot_state(i,1)
        self.wait()
        i = array.access_random_slot()
        array.set_slot_state(i,1)
        self.wait()
        i = array.access_random_slot()
        array.set_slot_state(i,1)
        self.wait()
        i = array.access_random_slot()
        array.set_slot_state(i,1)
        array.set_slot_state(i,0)
        self.wait()

        
class ArrayIndicate(Scene):
    def construct(self):
        a = Array(size=4,scene=self)
        self.add(a)
        self.play(a.write(2,'a'))
        a.indicate_index(2)
        self.wait()
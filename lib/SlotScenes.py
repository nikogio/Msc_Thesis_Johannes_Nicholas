from manim import *
from DataStructures.Slot import Slot


class SlotExample(Scene):  
    def construct(self):

        # create the slot
        slot = Slot(value=1)
        self.play(Write(slot))
        self.play(slot.remove_value())
        self.play(slot.set_value(2))
        self.play(slot.remove_value())
        self.play(slot.set_value(4))
        self.play(slot.animate.shift(2*LEFT),run_time=1)
        self.wait()
        slot2 = Slot(label=1).next_to(slot,buff=0.5)
        self.play(Write(slot2))
        self.play(slot2.set_value(3))
        self.play(slot2.remove_value())
        self.play(slot2.set_value(5))
        self.play(slot2.animate.scale(0.5))

class SlotExampleHashTable(Scene):
        def construct(self):
            # create slot1
            slot1 = Slot(hash_table=True)
            slot1.set_value(1)
            self.play(Create(slot1))

            slot2 = Slot(side_length=1.0,hash_table=True)
            slot2.set_value(1)
            slot2.shift(2*RIGHT)
            self.play(Create(slot2))

class SlotRectangle(Scene):
     def construct(self):  
        s = Slot(side_length=1)
        s1 = Slot(side_length=1).shift(RIGHT)
        self.play(Create(s))
        self.play(Create(s1))
        s.label_to_dots()
        self.play(s.animate.stretch(1.5,1))
        self.play(s1.animate.stretch(1.5,1))
        s1.label_to_dots()
        self.wait()

class SlotState(Scene):
     def construct(self):
          s = Slot()
          self.add(s)
          self.wait()
          s.set_state(1)
          self.wait()
          s.set_state(2)
          self.wait()
          s.set_state(0)

class SlotIndicate(Scene):
     def construct(self):
        s = Slot()
        #s.set_value('a')
        s.set_fill(opacity=0)
        self.add(s)
        self.play(Indicate(s))
        
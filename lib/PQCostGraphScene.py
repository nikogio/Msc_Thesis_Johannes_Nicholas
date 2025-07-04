from manim import * 
from DataStructures.ResizingArray import Stack

class Display(Scene):
    def construct(self):
        #plane = NumberPlane()
        #self.add(plane)
        horizontal_line = Line([-10,-1.5,0],[10,-1.5,0])
        vertical_line = Line([0,-1.5,0],[0,-10,0])
        self.add(horizontal_line,vertical_line)
        action_title = Text('Action:').move_to([-3.5,-2,0])
        self.action_text = None
        cost_title = Text('Cost:').move_to([3.5,-2,0])
        self.cost_text = None
        self.add(action_title,cost_title)
        self.add_stack()
        self.push(1)
        self.push(2)
        self.push(3)
        self.push(4)
        self.pop()
        self.pop()
        self.pop()
        self.pop()

    def add_stack(self):
        stack = Stack(scene=self)
        self.stack = stack

    def push(self,value):
        # Make action and cost text
        action_text = Text('Push: ('+str(value)+')',color=GREEN)
        cost_text = Text('1',color=GREEN)
        if self.stack.is_full():
            action_text.set_color(RED)
            cost_text = Text('4n+1',color=RED)
        # Setup action text
        self.action_text_to_place(action_text)
        self.old_action_text = self.action_text
        self.action_text = action_text
        # Setup cost text
        self.cost_text_to_place(cost_text)
        self.old_cost_text = self.cost_text
        self.cost_text = cost_text
        # Play all text
        self.play_text()
        # Execute push
        self.stack.push(value)


    def pop(self):
        # Make action and cost text
        action_text = Text('Pop()',color=GREEN)
        cost_text = Text('1',color=GREEN)
        if self.stack.needs_decrease():
            action_text.set_color(RED)
            cost_text = Text('3/2n+(n-1)',color=RED)
        # Setup action text
        self.action_text_to_place(action_text)
        self.old_action_text = self.action_text
        self.action_text = action_text
        # Setup cost text
        self.cost_text_to_place(cost_text)
        self.old_cost_text = self.cost_text
        self.cost_text = cost_text
        self.play_text()
        #Execute pop
        self.stack.pop()

    def action_text_to_place(self,text:Text):
        text.move_to([-3.5,-3,0])
    
    def cost_text_to_place(self,text:Text):
        text.move_to([3.5,-3,0])

    def play_text(self):
      chosen_lag_ratio=0.15
      self.play(AnimationGroup(AnimationGroup(
                                FadeOut(self.old_action_text),
                                FadeIn(self.action_text),
                                lag_ratio=chosen_lag_ratio),
                               AnimationGroup(
                                FadeOut(self.old_cost_text),
                                FadeIn(self.cost_text),
                                lag_ratio=chosen_lag_ratio
                                )))
      self.play(AnimationGroup(
          Indicate(self.action_text),
          Indicate(self.cost_text),
          lag_ratio=0
      ))
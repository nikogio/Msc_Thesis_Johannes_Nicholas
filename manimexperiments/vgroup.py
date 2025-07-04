from manim import *

class VGroupExp1(Scene):
    def construct(self):
        red = Circle().set_fill(RED)
        blue = Circle().set_fill(BLUE,opacity=0.5)
        green = Circle().set_fill(GREEN)
        v = VGroup(red)
        self.play(Create(v))
        self.play(red.animate.shift(LEFT))
        self.wait
        v.add(blue)
        self.play(Create(v))
        self.play(Indicate(v[3]))
        self.wait

class TestSquare(Scene):
    def construct(self):
        s = Square()
        d = Dot().move_to(s.get_right())
        self.add(s,d)

class ScaleObjects(Scene):
    def construct(self):
        # Create a VGroup of objects
        s1 = Square()
        s2 = Square(side_length=4)
        self.add(s1,s2)
        while s2.get_bottom()[1]<=s1.get_bottom()[1]:
            self.play(s2.animate.stretch(0.98,1))
       

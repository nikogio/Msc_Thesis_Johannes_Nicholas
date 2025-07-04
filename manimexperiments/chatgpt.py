from manim import *

class SquareWithText(Mobject):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.square = Square()
        self.text = Text(text)
        self.add(self.square, self.text)
        self.text.move_to(self.square)

    def set_text(self, new_text):
        self.text.become(Text(new_text))
        self.text.move_to(self.square)

class SquareWithTextExample(Scene):
    def construct(self):
        square_with_text = SquareWithText("Hello, World!")
        self.add(square_with_text)
        self.wait(1)
        square_with_text.set_text("New Text")
        self.wait(1)
        self.play(FadeOut(square_with_text))

class CircleObject(VMobject):
    def __init__(self, color=RED, radius=1, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(color=color, radius=radius)
        self.add(self.circle)

    def add_new_square(self, color=BLUE, side_length=0.5):
        self.square = Square(color=color, side_length=side_length).next_to(self.circle, RIGHT, buff=0.5)
        self.add(self.square)
        return (Create(self.square))
    
    def flip_square(self):
        try:
            return Rotate(self.square)
        except:
            None

    def indicate_circle(self):
        try:
            return Indicate(self.circle)
        except:
            None
    
    def flip_indicate(self):
        try:
            ani1 = self.flip_square()
            ani2 = self.indicate_circle()
            return AnimationGroup(ani1,
                                  ani2)
        except:
            None
    
    def flip_then_indicate(self):
        try:
            ani1 = self.flip_square()
            ani2 = self.indicate_circle()
            return Succession(ani1,
                                  ani2)
        except:
            None

class MyScene(Scene):
    def construct(self):
        circle_object = CircleObject()
        self.play(Create(circle_object))
        self.wait(1)
        self.play(circle_object.add_new_square())
        self.wait(1)
        self.play(circle_object.flip_square())
        self.play(circle_object.indicate_circle())
        self.wait()
        self.play(circle_object.flip_indicate())
        self.wait()
        self.play(circle_object.flip_then_indicate())


class TwoSquares(Scene):
    def construct(self):
        side_length = 2
        square1 = Square(side_length=side_length, color=BLUE)
        square2 = Square(side_length=side_length, color=RED)
        square2.shift((side_length * LEFT) + (side_length * DOWN))
        self.play(Create(square1), Create(square2))
        self.wait()
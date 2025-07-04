import math
from manim import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(RED, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen

class WriteText(Scene):
    def construct(self):
        text = Text("Hello World")
        self.play(Write(text))

class CreateCircle2(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(RED, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        square.next_to(circle, RIGHT, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen

class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        square = Square()  # create a square

        self.play(Create(square))  # show the square on screen
        self.play(square.animate.rotate(PI / 4))  # rotate the square
        self.play(
            ReplacementTransform(square, circle)
        )  # transform the square into a circle
        self.play(
            circle.animate.set_fill(PINK, opacity=0.5)
        )  # color the circle on screen
        self.play(circle.animate.flip())
        self.play(circle.animate.shift(1*DOWN))
        self.play(circle.animate.shift(1*LEFT))
        self.play(circle.animate.shift(1*UP))
        self.play(circle.animate.shift(1*RIGHT))
        self.play(FadeOut(circle))

        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()

class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()

class PolygonExample(Scene):
    def construct(self):
        isosceles = Polygon([-5, 1.5, 0], [-2, 1.5, 0], [-3.5, -2, 0])
        position_list = [
            [4, 1, 0],  # middle right
            [4, -2.5, 0],  # bottom right
            [0, -2.5, 0],  # bottom left
            [0, 3, 0],  # top left
            [2, 1, 0],  # middle
            [4, 3, 0],  # top right
        ]
        square_and_triangles = Polygon(*position_list, color=PURPLE_B)
        self.add(isosceles, square_and_triangles)

class PositioningDots(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)

        red_dot = Dot(color=RED)
        self.play(Create(red_dot))
        v=VGroup()
        v.add(red_dot)
        self.play(v.animate.shift(2*LEFT),run_time=2)

        g_d = Dot(color=GREEN)
        g_d.next_to(red_dot,RIGHT,buff=0.25)
        self.play(Create(g_d))
        b_d = Dot(color=BLUE_A)
        b_d.next_to(g_d,UP,buff=0.25)
        self.play(Create(b_d))

class Swapping(Scene):
    def construct(self):
        c = Circle()
        self.add(c)
        s = Square().next_to(c,RIGHT,buff = 2)
        self.play(Swap(c,s))
        self.play(Indicate(c))

class StillImage(Scene):
    def construct(self):
        c = Circle().shift(2.5*LEFT).set_fill(opacity=0.5)
        s = Square().set_fill(BLUE,opacity=0.5)
        self.add(c,s)

class IndicateAndMove(Scene):
    def construct(self):
        c = Circle().shift(2.5*LEFT).set_fill(opacity=0.5)
        self.add(c)
        self.play(Indicate(c))
        self.play(c.animate.shift(2.5*RIGHT))
        self.play(AnimationGroup(
            Indicate(c),
            c.animate.shift(2.5*LEFT)
        ))

class ScalingTest(Scene):
    def construct(self):
        d = Dot(radius = 0.3)
        self.add(d)
        self.play(d.animate.scale(0.5))
        self.play(d.animate.shift(LEFT*2))
        second = Dot(radius=d.radius)
        self.play(Create(second))

class AnimGroupTest(Scene):
    def construct(self):
        d = Dot()
        self.add(d)
        d2 = Dot(color=RED).shift(LEFT)
        shift_animation = d.animate.shift(RIGHT)
        self.play(AnimationGroup(
            shift_animation,
            #self.add(d2)
        ))

class ArcTest(Scene):
    def construct(self):
        a = Line()
        self.add(a)
        d = Arc().move_to(a.get_end())
        self.add(d)

class LineAndArc(Scene):
    def construct(self):
        for x in range(-7, 8):
            for y in range(-4, 5):
                self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))
        arc = ArcBetweenPoints(start = [-2,2,0],end=[2,2,0],angle=math.radians(240))
        arc1 = ArcBetweenPoints(start=[2,2,0],end=[2.2,2.2,0]).rotate(math.radians(180))
        arc2 = ArcBetweenPoints(start=[-2,2,0],end=[-2.2,2.2,0])
        self.add(arc,arc1,arc2)

class RectangleWithInvisibleSide(Scene):
    def construct(self):
        # Create a rectangle
        rectangle = Rectangle(
            width=3,
            height=2,
            fill_opacity=0,  # Adjust the fill opacity to make it semi-transparent
        )
        self.add(rectangle)
        line = Line(start=rectangle.get_corner(UL),end=rectangle.get_corner(UR),color=None)
        line.set_z_index(1)
        self.add(line)

class ScalingTest(Scene):
    def construct(self):
        s1 = Square(4)
        s1.scale(0.5)
        self.add(s1)
        s2 = Square(side_length=s1.side_length,color=YELLOW)
        self.add(s1,s2)

class ScreenRec(Scene):
    def construct(self):
        lower_rec = Rectangle(height=4.0,width=14.0).move_to([0,-2,0])
        upper_rec = Rectangle(height=4.0,width=14.0).move_to([0,2,0])


        self.add(lower_rec,upper_rec)
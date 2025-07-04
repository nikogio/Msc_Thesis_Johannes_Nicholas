from manim import *


class HelloWorld(Scene):
    def construct(self):
        text = Text('Hello world').scale(3)
        self.add(text)


class TextAlignment(Scene):
    def construct(self):
        title = Tex("K-means clustering and Logistic Regression", color=WHITE)
        title.scale(0.75)
        self.add(title.to_edge(UP))

        t1 = Tex("1. Measuring").set_color(WHITE)

        t2 = Tex("2. Clustering").set_color(WHITE)

        t3 = Tex("3. Regression").set_color(WHITE)

        t4 = Tex("4. Prediction").set_color(WHITE)

        x = VGroup(t1, t2, t3, t4).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.7).next_to(ORIGIN,DR)
        x.set_opacity(0.5)
        x.submobjects[1].set_opacity(1)
        self.add(x)
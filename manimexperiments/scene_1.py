from manim import *
import numpy as np

class CoordSysExample(Scene):
    def construct(self):
        # the location of the ticks depends on the x_range and y_range.
        grid = Axes(
            x_range=[0, 1, 0.05],  # step size determines num_decimal_places.
            y_range=[0, 1, 0.05],
            x_length=9,
            y_length=5.5,
            axis_config={
                "numbers_to_include": np.arange(0, 1+0.1, 0.1),
                "font_size": 24,
            },
            tips=False,
        )

        # Labels for the x-axis and y-axis.
        y_label = grid.get_y_axis_label("y", edge=LEFT, direction=LEFT, buff=0.4)
        x_label = grid.get_x_axis_label("x")
        grid_labels = VGroup(x_label, y_label)

        graphs = VGroup()
        for n in np.arange(1, 20 + 0.5, 0.5):
            graphs += grid.plot(lambda x: x ** n, color=RED)
            graphs += grid.plot(
                lambda x: x ** (1 / n), color=WHITE, use_smoothing=False
            )

        # Extra lines and labels for point (1,1)
        graphs += grid.get_horizontal_line(grid.c2p(1, 1, 0), color=BLUE)
        graphs += grid.get_vertical_line(grid.c2p(1, 1, 0), color=BLUE)
        graphs += Dot(point=grid.c2p(1, 1, 0), color=YELLOW)
        graphs += Tex("(1,1)").scale(0.75).next_to(grid.c2p(1, 1, 0))
        title = Title(
            # spaces between braces to prevent SyntaxError
            r"Graphs of $y=x^{ {1}\over{n} }$ and $y=x^n (n=1,2,3,...,20)$",
            include_underline=False,
            font_size=40,
        )

        self.add(title, graphs, grid, grid_labels)


class CoordSysExample2(Scene):
    def construct(self):
        # the location of the ticks depends on the x_range and y_range.
        grid = Axes(
            x_range=[0, 1, 0.05],  # step size determines num_decimal_places.
            y_range=[0, 1, 0.05],
            x_length=9,
            y_length=5.5,
            axis_config={
                "numbers_to_include": np.arange(0, 1+0.1, 0.1),
                "font_size": 24,
            },
            tips=False,
        )
        # Labels for the x-axis and y-axis.
        y_label = grid.get_y_axis_label("y", edge=LEFT, direction=LEFT, buff=0.4)
        x_label = grid.get_x_axis_label("x")
        grid_labels = VGroup(x_label, y_label)

        coord = grid.coords_to_point(0.1,0.1)
        dot = Dot(coord)

        coord2 = grid.coords_to_point(0.2,0.1)
        dot2 = Dot(coord2)

        self.add(grid, grid_labels,dot,dot2)

        self.play(grid.animate.scale(0.5))

class Test(Scene):
    def construct(self):
        y_min, y_max = ValueTracker(0), ValueTracker(100)
        y_tick_step = ValueTracker(y_max.get_value()/10)

        ax = always_redraw(lambda: Axes(
            x_range=[0, 60, 15],
            y_range=[y_min.get_value(), y_max.get_value(), y_tick_step.get_value()],
            tips=False,
            axis_config={"include_numbers": True}
        ))

        self.add(ax)
        
        self.play(AnimationGroup(
                y_min.animate.set_value(0),
                y_max.animate.set_value(200),
                y_tick_step.animate.set_value(y_max.get_value()/10)))

        self.wait(5)

class Test_Discord(Scene):
    def construct(self):

        default_y_ticks_list = [10, 20, 50, 100] # Beginning ticks of graph
        default_x_ticks_list = [10, 20, 50, 100] # Beginning ticks of graph


        def build_axes(x_range, y_range, y_tick_list, x_tick_list):
            return Axes(
                x_range=x_range,
                y_range=y_range,
                tips=False,
                axis_config={"include_numbers": True},
                y_axis_config={
                    "numbers_to_include": default_y_ticks_list,
                    "numbers_with_elongated_ticks": default_y_ticks_list,
                    "include_ticks": True,
                    "tick_size": 0.001,
                    "longer_tick_multiple": 100,},
                x_axis_config={
                    "numbers_to_include": default_x_ticks_list,
                    "numbers_with_elongated_ticks": default_x_ticks_list,
                    "include_ticks": True,
                    "tick_size": 0.001,
                    "longer_tick_multiple": 100,
                }
            )

        # Add method description
        def get_ticks_list(new_max,
                           axes_tick_list):# The tick_list of the axes you are working with
            if new_max > axes_tick_list[-1]:
                axes_tick_list.append(new_max)
                axes_tick_list.pop(0)
            return axes_tick_list

        ax = build_axes(x_range=[0,default_x_ticks_list[-1]],
                        y_range=[0, default_y_ticks_list[-1]],
                        y_tick_list=default_y_ticks_list, # Makes the original axes.
                        x_tick_list = default_x_ticks_list)
        self.add(ax) # Adding axes to Scene
        self.wait()

        previous_y = default_y_ticks_list[-1]
        previous_x = default_x_ticks_list[-1]
        current_y_tick_list = default_y_ticks_list
        current_x_tick_list = default_x_ticks_list

        for new_max_value in [130, 160, 200, 250]:

            # Below code grows y-axis to a larger y-axis, but with the same ticks.
            smaller_ax = build_axes(x_range=[0, new_max_value],
                                    y_range=[0, new_max_value],
                                    y_tick_list=get_ticks_list(previous_y,current_y_tick_list),
                                    x_tick_list = get_ticks_list(previous_x,current_x_tick_list))
            self.play(Transform(ax, smaller_ax))


            # self.wait(2) # Waiting to easier display separate animations, don't include in final product.

            # Creating the new tick lists.
            current_y_tick_list = get_ticks_list(new_max_value, current_y_tick_list)
            current_x_tick_list = get_ticks_list(new_max_value, current_x_tick_list)

            # Instantiating new axis with a higher max tick AND without the current lowest tick.
            new_ax = build_axes(x_range=[0,new_max_value], y_range=[0, new_max_value],
                                y_tick_list=current_y_tick_list,
                                x_tick_list=current_x_tick_list)
            
            
            
            # Replacing current axis with new axis.
            self.play(AnimationGroup(
                FadeOut(ax),
                FadeIn(new_ax)
            ))
            #self.remove(ax)
            #self.wait(2)
            #self.add(new_ax)

            # Renaming to continue loop.
            ax = new_ax
            previous_y = new_max_value
            previous_x = new_max_value
            self.wait(1)
        self.wait()
        
        
class AddingDots(Scene):
    def construct(self):
        dot = Dot(color = "BLUE")
        ax = Axes(x_range=[0, 10], y_range=[0, 10])
        self.add(ax)
        dot.move_to(ax.c2p(1, 10))
        self.play(FadeIn(dot)) 
        #moving dot 
        self.play(dot.animate.move_to(ax.c2p(4, 10)))
        
        dot2 = Dot(color = "RED")
        dot2.move_to(ax.c2p(2, 7))
        self.play(FadeIn(dot2))
        self.play(dot2.animate.move_to(ax.c2p(4, 7)))
        

class DotsMoving(Scene):
    def construct(self):
        dots = [Dot() for i in range(3)]
        directions = [np.random.randn(3) for dot in dots]
        self.add(*dots) # It isn't absolutely necessary
        animations = [ApplyMethod(dot.shift,direction) for dot,direction in zip(dots,directions)]
        #since animations are object, we make a list, then play each of them with *
        self.play(*animations) # * -> unpacks the list animations


class MovingDotsChangingAxes(Scene):
    def construct(self):
        dots = []
        default_y_ticks_list = [10, 20, 50, 100] # Beginning ticks of graph
        default_x_ticks_list = [10, 20, 50, 100] # Beginning ticks of graph


        def build_axes(x_range, y_range, y_tick_list, x_tick_list):
            return Axes(
                x_range=x_range,
                y_range=y_range,
                tips=False,
                axis_config={"include_numbers": True},
                y_axis_config={
                    "numbers_to_include": default_y_ticks_list,
                    "numbers_with_elongated_ticks": default_y_ticks_list,
                    "include_ticks": True,
                    "tick_size": 0.001,
                    "longer_tick_multiple": 100,},
                x_axis_config={
                    "numbers_to_include": default_x_ticks_list,
                    "numbers_with_elongated_ticks": default_x_ticks_list,
                    "include_ticks": True,
                    "tick_size": 0.001,
                    "longer_tick_multiple": 100,
                }
            )

        def addDots(axes,x, y):
            dot = Dot(color = "BLUE")
            dot.move_to(axes.c2p(x, y))
            dots.append(dot)
            self.play(Create(dot))
            
        def moveDots(old_axes, new_axes):
            oldpositions = [old_axes.p2c(dot.get_center()) for dot in dots]
            animations = [ApplyMethod(dot.move_to, new_axes.c2p(*oldposition)) for dot, oldposition in zip(dots, oldpositions)]
            #loop through list of dots and move them to new axes
            return animations #return animations to play them later
        
        
            
        # Add method description
        def get_ticks_list(new_max,
                           axes_tick_list):# The tick_list of the axes you are working with
            if new_max > axes_tick_list[-1]:
                axes_tick_list.append(new_max)
                axes_tick_list.pop(0)
            return axes_tick_list

        ax = build_axes(x_range=[0,default_x_ticks_list[-1]],
                        y_range=[0, default_y_ticks_list[-1]],
                        y_tick_list=default_y_ticks_list, # Makes the original axes.
                        x_tick_list = default_x_ticks_list)
        self.add(ax) # Adding axes to Scene
        self.wait()
        #creating Dots 
        addDots(ax, 1, 10)
        addDots(ax, 2, 7)
        addDots(ax, 3, 5)
        addDots(ax, 4, 3)
        
        previous_y = default_y_ticks_list[-1]
        previous_x = default_x_ticks_list[-1]
        current_y_tick_list = default_y_ticks_list
        current_x_tick_list = default_x_ticks_list

        for new_max_value in [130, 160, 200, 250]:

            # Below code grows y-axis to a larger y-axis, but with the same ticks.
            smaller_ax = build_axes(x_range=[0, new_max_value],
                                    y_range=[0, new_max_value],
                                    y_tick_list=get_ticks_list(previous_y,current_y_tick_list),
                                    x_tick_list = get_ticks_list(previous_x,current_x_tick_list))
            moving_dots_animation = moveDots(ax, smaller_ax)
            self.play(AnimationGroup(
                Transform(ax, smaller_ax)),
                *moving_dots_animation)
            

            # self.wait(2) # Waiting to easier display separate animations, don't include in final product.

            # Creating the new tick lists.
            current_y_tick_list = get_ticks_list(new_max_value, current_y_tick_list)
            current_x_tick_list = get_ticks_list(new_max_value, current_x_tick_list)

            # Instantiating new axis with a higher max tick AND without the current lowest tick.
            new_ax = build_axes(x_range=[0,new_max_value], y_range=[0, new_max_value],
                                y_tick_list=current_y_tick_list,
                                x_tick_list=current_x_tick_list)
            
            
            
            # Replacing current axis with new axis.
            self.play(AnimationGroup(
                FadeOut(ax),
                FadeIn(new_ax)
            ))
            #self.remove(ax)
            #self.wait(2)
            #self.add(new_ax)

            # Renaming to continue loop.
            ax = new_ax
            previous_y = new_max_value
            previous_x = new_max_value
            self.wait(1)
        self.wait()
    
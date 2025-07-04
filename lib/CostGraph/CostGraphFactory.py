from manim import *
class CostGraphFactory:
    def __init__(self,x_length, y_length):
        self.x_length = x_length
        self.y_length = y_length
        
    def build_axes(self,x_range, y_range, y_tick_list, x_tick_list):
            return Axes(
                x_range=x_range,
                y_range=y_range,
                x_length=self.x_length,
                y_length=self.y_length,
                tips=False,
                axis_config={"include_numbers": True},
                y_axis_config={
                    "numbers_to_include": y_tick_list,
                    "numbers_with_elongated_ticks": y_tick_list,
                    "include_ticks": True,
                    "tick_size": 0.001,
                    "longer_tick_multiple": 100,},
                x_axis_config={
                    "numbers_to_include": x_tick_list,
                    "numbers_with_elongated_ticks": x_tick_list,
                    "include_ticks": True,
                    "tick_size": 0.001,
                    "longer_tick_multiple": 100,
                }
            )
    def generate_new_tick_list(self,new_max,axes_tick_list):
        if new_max > axes_tick_list[-1]:
            axes_tick_list.append(new_max)
            axes_tick_list.pop(0)
        return axes_tick_list


    def create_graph(self,
                     x_tick_list,
                     y_tick_list,
                     resize_x=False,
                     resize_y=False):
        if resize_x:
            new_x_max = (x_tick_list[-1])*2 
            x_tick_list = self.generate_new_tick_list(new_x_max,x_tick_list)
        if resize_y:
            new_y_max = (y_tick_list[-1])*2
            y_tick_list = self.generate_new_tick_list(new_y_max,y_tick_list)

        axes = self.build_axes(x_range=([0,x_tick_list[-1]]),
                                    y_range=[0,y_tick_list[-1]],
                                    x_tick_list= x_tick_list,
                                    y_tick_list= y_tick_list)
        return axes
        
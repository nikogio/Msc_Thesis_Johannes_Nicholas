from manim import *
import numpy as np
import math
from DataStructures.NodeFactory import NodeFactory
from DataStructures.Node import Node

class BagAbstract(VMobject):
    def __init__(self,
                 scene:Scene,
                 start_point=np.array([-2,2,0]), # Left top point of Arc
                 end_distance_from_start:float=4.0, # Distance of right top point of Arc from start
                 ):
        self.scene=scene

        # Setup of bag visuals
        end_point = start_point+[end_distance_from_start,0,0]
        self.arc = ArcBetweenPoints(start = start_point,
                                    end=end_point,
                                    angle=math.radians(240))
        self.invis_circle = Circle(radius=self.arc.get_width()/2).move_to(self.arc.get_arc_center())
        self.detail_arc_left = ArcBetweenPoints(start=start_point,end=start_point+[-0.2,0.2,0])
        self.detail_arc_right = ArcBetweenPoints(start=end_point,end=end_point+[0.2,0.2,0]).rotate(math.radians(180))
        self.invis_line = Line(start=start_point,end = end_point)
        # Adding to scene.
        self.scene.add(self.arc,self.detail_arc_left,self.detail_arc_right)
        # Trackers list and factory for Nodes
        self.nodes = []
        self.node_factory = NodeFactory()
        self.vgroup = VGroup(self.arc,self.invis_circle,self.invis_line,self.detail_arc_left,self.detail_arc_right)
              
    def create_node(self,value):
        #Create a node object scaled 
        node = self.node_factory.create_node(value=value,radius=(0.1*self.invis_circle.radius))
        self.vgroup.add(node)
        self.nodes.append(node)
        return node
    
    def put(self,value):
        # Finding position for Node in Bag
        position = None
        invi_circle_center = self.invis_circle.get_center()
        c = invi_circle_center[0:2]
        while True:
            x = np.random.uniform(-self.invis_circle.radius, self.invis_circle.radius)
            y = np.random.uniform(-self.invis_circle.radius, self.invis_circle.radius)
            eucl_dist = np.linalg.norm([x,y] - c)
            y_dist = self.invis_line.get_center()[1]-c[1:]
            if eucl_dist<self.invis_circle.radius*0.95 and y < y_dist:
                position = invi_circle_center + np.array([x, y, 0])
                break
        # Creating Node
        node = self.create_node(value)
        node.move_to(position)
        self.scene.play(Create(node))
    
    def pull(self,value):
        for x in self.nodes:
            if x.get_value()==value:
                self.scene.play(FadeOut(x))
                self.nodes.remove(x)
                self.vgroup.remove(x)
            break
from manim import *
from DataStructures.NodeFactory import NodeFactory

class StackAbstract(VMobject):
    def __init__(self,
                 scene:Scene,
                 width:float=2.0,height:float=4.0,
                 location:np.array=[0,0,0],
                 **kwargs):
        super().__init__(**kwargs)
        self.scene=scene
        self.width = width
        self.height = height
        self.open_rec = OpenRectangle(width,height,center=location)
        self.add(self.open_rec)
        self.scene.add(self.open_rec)
        self.node_factory = NodeFactory()
        self.nodes = []
        self.vgroup = VGroup()
        self.current_node_scale = 1
        self.scene.play(Create(self.vgroup))

    def push(self,value):
        # Case 1, Stack is empty.
        if len(self.nodes)==0: # Case 1 (Q is empty) -> Move to start position
            position = self.open_rec.lower_line.get_center()+np.array([0,self.height*0.075*self.current_node_scale, 0])
        else: # Case 2 -> Move behind last dot in line
            previous_node = self.nodes[len(self.nodes)-1]
            position = previous_node.get_center()+[0,self.height*0.075*self.current_node_scale*2,0]
            # Case 3, Stack overflowing -> Scale down node size.
            if position[1]>=self.open_rec.upper_line.get_center()[1]:
                 self.scale_node_size_down()
                 previous_node = self.nodes[len(self.nodes)-1]
                 position = previous_node.get_center()+[0,self.height*0.075*self.current_node_scale*2,0]
        node = self.node_factory.create_node(value=value,radius=self.height*0.075*self.current_node_scale)
        node.move_to(self.open_rec.upper_line.get_center()+[0,0.3,0])
        self.nodes.append(node)
        self.vgroup.add(node)
        self.scene.play(Create(node))
        self.scene.play(node.animate.move_to(position))


    # For some reason, the last node cannot be popped.
    # This needs investigation.
    def pop(self):
        # Remove top node
        node = self.nodes[len(self.nodes)-1]
        self.scene.play(node.animate.move_to(self.open_rec.upper_line.get_center()+[0,0.3,0]))
        self.scene.play(FadeOut(node))
        self.nodes.remove(node)
        self.vgroup.remove(node)

        # Now check for and execute resizing.
        top_node_pos = self.nodes[len(self.nodes)-1].get_center()
        if top_node_pos[1]<=self.open_rec.lower_line.get_center()[1]+1/4*self.height: # Stack is less than 1/4 full.
            self.scale_node_size_up()

            
    def scale_node_size_down(self):
        self.current_node_scale/=2
        self.scale_nodes()
        self.move_nodes_new_positions()
            

    def scale_node_size_up(self):
        if self.current_node_scale<1:
            self.current_node_scale*=2
            self.move_nodes_new_positions()
            self.scale_nodes()

    def scale_nodes(self):
        temp_nodes=[]
        for i in range(len(self.nodes)):
            replacement_node = self.node_factory.create_node(value=self.nodes[i].get_value(),radius=self.height*0.075*self.current_node_scale)
            replacement_node.move_to(self.nodes[i].get_center())
            temp_nodes.append(replacement_node)
            self.vgroup.remove(self.nodes[i])
            self.vgroup.add(replacement_node)
        #nodes_scaling = [ApplyMethod(node.scale,self.current_node_scale) for node in self.nodes]
        nodes_scaling = [ReplacementTransform(self.nodes[i],temp_nodes[i])for i in range(len(self.nodes))]
        for i in range(len(self.nodes)):
            self.nodes[i] = temp_nodes[i]
        self.scene.play(AnimationGroup(*nodes_scaling))

    def move_nodes_new_positions(self):
        # Moving nodes into new places.
        first_node = self.nodes[0]
        first_node_move = first_node.animate.move_to(self.open_rec.lower_line.get_center()+np.array([0,self.height*0.075*self.current_node_scale, 0]))
        new_positions = [self.open_rec.lower_line.get_center()+[0,(x+1.5)*self.height*0.075*self.current_node_scale*2,0] for x in range(len(self.nodes)-1)]
        nodes_move = [ApplyMethod(node.move_to,position) for node,position in zip(self.nodes[1:],new_positions)]
        self.scene.play(AnimationGroup(first_node_move,
                                       *nodes_move,
                                       lag_ratio=0))


# Helper class for StackAbstract. Provides the open Rectangle.
class OpenRectangle(VMobject):
    def __init__(self,width:float=2.0,height:float=4.0,
                 open_side:str='up',
                 center:np.array=[0,0,0],
                 **kwargs):
        super().__init__(**kwargs)
        self.left_line = Line(start=ORIGIN,end =ORIGIN+[0,height,0])
        self.lower_line = Line(start=self.left_line.get_start(),
                               end = self.left_line.get_start()+[width,0,0])
        self.right_line = Line(start=self.lower_line.get_end(),
                               end=self.lower_line.get_end()+[0,height,0])
        self.upper_line = Line(start=self.left_line.get_end(),end = self.right_line.get_end())
        self.add(self.left_line,self.lower_line,self.right_line,self.upper_line)
        self.move_to(center)
        if open_side=='lower':
            self.remove(self.lower_line)
        elif open_side=='left':
            self.remove(self.left_line)
        elif open_side=='right':
            self.remove(self.right_line)
        else:
            self.remove(self.upper_line)
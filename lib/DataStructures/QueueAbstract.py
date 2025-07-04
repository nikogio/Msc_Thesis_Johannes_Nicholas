from manim import *
from DataStructures.NodeFactory import NodeFactory

class QueueAbstract(VMobject):
    def __init__(self,
                 scene:Scene,
                 height=3.0,
                 width=6.0,
                 **kwargs):
        super().__init__(**kwargs)
        self.scene=scene
        #Setup of Rectangle
        self.rectangle = Rectangle(height=height, width = width)
        self.add(self.rectangle)
        #Setup of Text
        self.text = Text("Entrance",width=height/2,height = width/10).rotate(270*DEGREES)
        self.text.next_to(self.rectangle.get_right(), LEFT).set_z_index(1)
        self.text.scale(0.5 * self.rectangle.height)
        self.add(self.text)
        #Setting up Line
        self.line = Line(self.rectangle.get_top(),self.rectangle.get_bottom()).next_to(self.text,LEFT)
        self.add(self.line)
        #Setting up VGroup, allowing movement of alle elements simultaneously.
        self.vgroup = VGroup(self.rectangle,self.text,self.line)
        #Setting up List of Nodes
        self.nodes=[]
        self.node_factory = NodeFactory()
        self.scene.add(self.vgroup)
        self.nodes_waiting=[]

    def enqueue(self,value):
        if len(self.nodes)==0: # Case 1 (Q is empty) -> Move to start position
            position = self.line.get_center()+np.array([-0.055*self.rectangle.width, 0, 0])
        else: # Case 2 -> Move behind last dot in line
            previous_node = self.nodes[len(self.nodes)-1]
            position = previous_node.get_center()+[-previous_node.circle.radius*2.1,0,0]
            if position[0]<=self.rectangle.get_left()[0]: # Case 3, no space in animation, wait outside the scene
                 self.nodes_waiting.append(value)
                 return
        node = self.node_factory.create_node(value,radius=self.rectangle.width*0.05)
        node.move_to(self.rectangle.get_left())
        self.scene.play(Create(node))
        self.nodes.append(node)
        self.vgroup.add(node)
        self.scene.play(node.animate.move_to(position))

    def dequeue(self):
        if len(self.nodes)==0:
            return None
        first_node = self.nodes[0]
        new_positions = [node.get_center() for node in self.nodes[:len(self.nodes)-1]]
        other_nodes_move = [ApplyMethod(node.move_to,position) for node,position in zip(self.nodes[1:],new_positions)]
        self.scene.play(AnimationGroup(FadeOut(first_node),
                                       *other_nodes_move,
                                       lag_ratio=0.15))
        #Clean up
        self.nodes.remove(first_node)
        self.vgroup.remove(first_node)

        # Add new node if queue was full and some were waiting.
        if len(self.nodes_waiting)>0:
            new_node = self.nodes_waiting[0]
            self.nodes_waiting.remove(new_node)
            self.vgroup.remove(new_node)
            self.enqueue(new_node)
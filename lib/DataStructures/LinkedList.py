from manim import *
#from HighAbstractionAnimations.NodeFactory import NodeFactory
from DataStructures.Node import Node

class LinkedList(VMobject):
    def __init__(self,scene:Scene,
                 radius:float=None,
                 line_length:float=0.5, # The length of lines between Nodes
                 origin=[0,0,0], # The origin of the first line of the LL.
                                             # This will in hash tables be the side
                                             # of an array slot.
                 **kwargs):
        super().__init__(**kwargs)
        self.scene = scene
        self.origin = origin
        self.line_length = line_length
        if radius:
            self.radius=radius
        else:
            self.radius = line_length
        #self.factory = NodeFactory()
        self.nodes=[]
        self.lines=[]
        self.vgroup = VGroup()
        self.add(self.vgroup)

    def add_value(self,value):
        # Creating the line in position
        if len(self.nodes)==0:
            line = Line(start = self.origin,
                        end = (self.origin+np.array([self.line_length,0,0])))
        else:
            line = Line(start = self.nodes[len(self.nodes)-1].get_center()+np.array([self.radius,0,0]),
                        end = self.nodes[len(self.nodes)-1].get_center()+np.array([self.radius+self.line_length,0,0]))
        # Creating Node in position relative to line.
        node = Node(value,self.radius)
        node.move_to(line.get_end()+[self.radius,0,0])
        # Adding to arrays to keep track.
        self.lines.append(line)
        self.nodes.append(node)
        #Playing creation animation
        self.scene.play(Create(line))
        self.scene.play(Create(node))
        #Adding to VMobject VGroup
        self.vgroup.add(line)
        self.vgroup.add(node)


    def remove_value(self,value):
        to_remove = self.search(value)
        self.remove_node_at_index(to_remove)

    def remove_value_no_search(self,value):
        to_remove=None
        for i in range(len(self.nodes)):
              if self.nodes[i].get_value()==value:
                to_remove=i
        if to_remove==None:
             raise ValueError("Value " + str(value) + " not present in linked list.")
        self.remove_node_at_index(to_remove)
        
    def remove_node_at_index(self,index):
         self.scene.play(FadeOut(self.lines[index],self.nodes[index]))
         if index<len(self.nodes)-1:
            temp_vgroup = VGroup()
            for i in range (index+1,len(self.nodes)):
                            temp_vgroup.add(self.lines[i])
                            temp_vgroup.add(self.nodes[i])
            position = self.lines[index].get_start()
            self.scene.play(temp_vgroup.animate.align_to(position,LEFT))
            line_to_remove = self.lines.pop(index)
            node_to_remove = self.nodes.pop(index)
            self.vgroup.remove(line_to_remove)
            self.vgroup.remove(node_to_remove)
        


    def search(self,value):
        current_node=0
        animations = []
        searching = True
        while searching and current_node<len(self.nodes):
            indication_line = Line(start=self.lines[current_node].get_start(),
                                   end = self.lines[current_node].get_end(),
                                   color=YELLOW).set_z_index(1)
            self.scene.play(Create(indication_line))
            new_indication_line = Line(start=indication_line.get_end(),
                                       end = indication_line.get_start(),
                                       color = YELLOW)
            self.scene.add(new_indication_line)
            self.scene.remove(indication_line)
            self.scene.play(Uncreate(new_indication_line))
            if self.nodes[current_node].get_value()==value:
                self.scene.play(Indicate(self.nodes[current_node],scale_factor=2,color=PURE_GREEN))
                searching = False
            else:
                self.scene.play(Indicate(self.nodes[current_node]))
                current_node+=1
        return current_node

    def get_length(self):
         return len(self.nodes)






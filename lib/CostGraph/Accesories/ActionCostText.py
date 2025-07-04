from manim import *
#a box where text should be placed, box can be moved around the scene  
class ActionCostText(VMobject):
    def __init__(self,
                 value:str=" ",
                 side_length: float = 5.0,
                 height: float = 4.0,
                 label: int =0, 
                 scene: Scene = None,
                stack: bool = False,
                queue: bool = False,
                bag: bool = False,
                  **kwargs):
        self.stack=stack
        self.queue=queue
        self.bag=bag
        self.rectangleBox = Rectangle(height=height, width=side_length, fill_color=BLUE, fill_opacity=0.15, stroke_color=WHITE, stroke_width=2.5)
        self.multiText = Text(str(value)).move_to(self.rectangleBox.get_center())
        self.group = VGroup(self.rectangleBox, self.multiText)
        self.scene = scene
        self.text = None
        # adding to scene
        self.scene.add(self.group)
        

    def generateText(self, adding: bool, costly: bool):
        if adding:
            if (self.stack):
                if costly:
                    self.text = "Action: Push()\nCost: 4n+1"
                else:
                    self.text = "Action: Push()\nCost: 1"
            if (self.bag):
                if costly:
                    self.text = "Action: Add()\nCost: 4n+1"
                else:
                    self.text = "Action: Add()\nCost: 1"
            if (self.queue):
                if costly:
                    self.text = "Action: Enqueue()\nCost: 4n+1"
                else:
                    self.text = "Action: Enqueue()\nCost: 1"
        else:
            if self.stack:
                if costly:
                    self.text = "Action: Pop()\nCost:4n+1"
                else:
                    self.text = "Action: Pop()\nCost: 1"
            if self.bag:
                if costly:
                    self.text = "Action: Remove()\nCost:4n+1"
                else:
                    self.text = "Action: Remove()\nCost: 1"
            if self.queue:
                if costly:
                    self.text = "Action: Dequeue()\nCost:4n+1"
                else:
                    self.text = "Action: Dequeue()\nCost: 1"


    def createText(self):
        oldText = self.multiText
        self.multiText = Text(self.text).move_to(self.rectangleBox.get_center())
        self.scene.play(AnimationGroup(FadeOut(oldText), FadeIn(self.multiText)))


        
    def writeText(self, adding: bool, costly: bool):
        self.generateText(adding, costly)
        self.createText()
        
        
class TextBox(Scene):
    def construct(self):
        textBox = ActionCostText(stack=True, scene=self)
        textBox.writeText(True, True)
        textBox.writeText(True, True)
        textBox.writeText(True, False)
        textBox.writeText(True, True)
        textBox.writeText(False, False)
        textBox.writeText(False, False)
        textBox.writeText(False, True)
        
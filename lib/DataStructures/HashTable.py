from manim import *
from DataStructures.Array import Array
from DataStructures.Slot import Slot
from DataStructures.ArrayFactory import ArrayFactory
from DataStructures.LinkedList import LinkedList


class HashTable(VMobject):
    def __init__(
        self,
        scene: Scene,
        side_length: float = 1.0,
        size: int = 4,
        screen_rectangle: Rectangle = Rectangle(
            height=8, width=14
        ),  # Default is full screen.
        max_ll_length: int = 3,
        resizing: bool = False,
        color_coding: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.screen_rectangle = screen_rectangle
        self.max_ll_length = max_ll_length
        self.resizing = resizing
        self.color_coding = color_coding
        self.array_factory = ArrayFactory(screen_rectangle=screen_rectangle)
        self.array = self.array_factory.create_initial_array(
            size=size, side_length=side_length, hash_table=True
        )
        self.scene = scene
        # self.add(self.array)
        self.vgroup = VGroup(self.array)
        self.scene.play(Create(self.array))
        self.linked_lists = []  # An array of arrays, holding the nodes of each chain.
        for i in range(size):
            ll = LinkedList(
                scene=self.scene,
                origin=self.array.slots[i].get_right(),
                line_length=0.4 * self.array.slots[i].square.side_length,
            )
            self.linked_lists.append(ll)
            self.vgroup.add(ll.vgroup)

    def add_value(self, value):
        # Calculate hash value
        hash = self.custom_hash(value, len(self.array.slots))
        # Check if it will be added to a linked list that is too long
        if self.linked_lists[hash].get_length() >= self.max_ll_length and self.resizing:
            # Trigger resizing:
            self.resizing_setup()
            # 1. Shrink and move original array
            self.shrink_old_hash_table()
            # Creating Array
            self.create_new_hash_table(doubling=True)
            # 3. Add all elements to new arrays linked lists.
            for i in range(len(self.old_array.slots)):
                self.scene.play(Indicate(self.old_array.slots[i]))
                for k in range(len(self.old_linked_lists[i].nodes)):
                    self.scene.play(Indicate(self.old_linked_lists[i].nodes[k]))
                    value_at_node = self.old_linked_lists[i].nodes[k].get_value()
                    self.regular_add_value(value_at_node)
            # 4. FadeOut original array
            self.fade_out_old_hash_table()

        # add_value to relevant linked list
        self.regular_add_value(value)

    def regular_add_value(self, value):
        hash = self.custom_hash(value, len(self.array.slots))
        for i in range(len(self.linked_lists[hash].nodes)):
            if self.linked_lists[hash].nodes[i].get_value() == value:
                self.scene.add(self.array.slots[hash])
                return
        self.linked_lists[hash].add_value(value)
        self.scene.add(self.array.slots[hash])


    def resizing_setup(self):
        self.old_array = self.array
        self.old_linked_lists = self.linked_lists
        self.old_vgroup = self.vgroup
        self.linked_lists = []
        self.vgroup = VGroup()

    def shrink_old_hash_table(self):
        self.scene.play(self.old_vgroup.animate.scale(0.4))
        self.scene.play(self.old_vgroup.animate.align_to(self.screen_rectangle, RIGHT))

    def create_resized_array(self, doubling: bool):
        self.array = self.array_factory.create_array(
            size=len(self.array.slots),
            ini_array=self.array,
            doubling=doubling,
            hash_table=True,
        )
        self.scene.play(Create(self.array))

    def create_new_hash_table(self, doubling: bool):
        self.create_resized_array(doubling)
        self.vgroup.add(self.array)  # references correct array?
        # Creating linked lists for array
        for i in range(len(self.array.slots)):
            ll = LinkedList(
                scene=self.scene,
                origin=self.array.slots[i].get_right(),
                line_length=0.4 * self.array.slots[i].square.side_length,
            )

            self.linked_lists.append(ll)
            self.vgroup.add(ll.vgroup)  # why are we adding vgroup of ll?
            # Each LL consists of a vgroup of objects.
            # (Nodes, lines). Adding them to the HT vgroup allows it all
            # to be manipulated at the same time.
            # Example: Shrinking.

    def fade_out_old_hash_table(self):
        self.scene.play(FadeOut(self.old_vgroup))

    # resizing to small values not implemented yet
    def remove_value(self, value):
        hash = self.custom_hash(value, len(self.array.slots))
        self.scene.play(Indicate(self.array.slots[hash]))
        self.linked_lists[hash].remove_value(value)

    def search_value(self, value):
        hash = self.custom_hash(value, len(self.array.slots))
        self.scene.play(Indicate(self.array.slots[hash]))
        self.linked_lists[hash].search(value)

    def custom_hash(self, char, bucket_size):
        if "a" <= char <= "z":
            return (ord(char) - ord("a")) % bucket_size
        else:
            raise ValueError("Input must be a lowercase letter from 'a' to 'z'")

    def turn_yellow(self):
        self.scene.play(self.vgroup.animate.set_color(YELLOW))

        
    def turn_grey(self):
        animations = []
        for i in range (len(self.array.slots)):
            animations.append(self.array.slots[i].square.animate.set_fill(GREY,1))
        self.scene.play(AnimationGroup(*animations))

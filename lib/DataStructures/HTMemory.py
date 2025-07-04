from manim import *
from DataStructures.Array import Array
from DataStructures.Memory import Memory
from DataStructures.HashTable import HashTable

class HTMemory(VMobject):
    def __init__(self,scene,
                 nr_of_lines:int=4,
                 slots_pr_line:int=20,
                 side_length_HT:float=1.0,
                 resizing:bool = False,
                 max_ll_length:int = 3,
                 size:int = 4,
                 color_coding:bool=False,
                 **kwargs):

        self.upper_R= Rectangle(height=4,width=14).move_to([0,1.9,0])
        self.lower_R= Rectangle(height=3,width=14).move_to([0,-2.5,0])
        self.scene=scene
        self.size = size
        self.color_coding=color_coding
        #initialise list of available colors
        self.available_colors = [
            BLUE_D,
            TEAL_D,
            GREEN_C,
            YELLOW_C,
            GOLD_A,
            RED_C,
            MAROON_A,
            PURPLE_C,]

        #Setting up HashTable  
        self.hash_table = HashTable(scene,
                        screen_rectangle=self.upper_R,
                         side_length=side_length_HT,
                         resizing=resizing,
                         max_ll_length = max_ll_length,
                         size=size,
                         color_coding=self.color_coding,
                         **kwargs)
        if self.color_coding:
            #assign colors to HT slots in order from available_colors
            for i in enumerate(self.hash_table.array.slots):
                self.hash_table.array.slots[i[0]].set_color(self.available_colors[i[0]])
        #Setting up Memory
        self.memory = Memory(screen_rect = self.lower_R,
                        slots_pr_line=slots_pr_line,
                        nr_of_lines=nr_of_lines,
                        scene=self.scene,color_coding=self.color_coding)
        self.ht_array = self.memory.select_random_slots(self.size) # The slots where the HT array is located.
        if self.color_coding:
            #assign colors to Memory slots in the same order from available_colors
            self.memory.set_multiple_slot_state(self.ht_array,1,self.available_colors)
        else:
            self.memory.set_multiple_slot_state(self.ht_array,1)

        #pairs for binding memory slots and HT nodes
        self.pairs = []
        
    def search(self,value):
        hash_value = self.hash_table.custom_hash(value,bucket_size = len(self.ht_array))
        #Indicate the array and memory slot
        self.scene.play(AnimationGroup(
                            Indicate(self.hash_table.array.slots[hash_value], color=WHITE),
                            Indicate(self.memory.slots[self.ht_array[hash_value]],color=WHITE)
        ))
        #Indicate Nodes + memory slots
        searching = True
        current_node = 0
        inspected_linked_list = self.hash_table.linked_lists[hash_value]
        while searching and current_node < len(inspected_linked_list.nodes):
            # Indication of line in hash table
            indication_line = Line(start=inspected_linked_list.lines[current_node].get_start(),
                                   end = inspected_linked_list.lines[current_node].get_end(),
                                   color=YELLOW).set_z_index(1)
            self.scene.play(Create(indication_line))
            new_indication_line = Line(start=indication_line.get_end(),
                                       end = indication_line.get_start(),
                                       color = YELLOW)
            self.scene.add(new_indication_line)
            self.scene.remove(indication_line)
            self.scene.play(Uncreate(new_indication_line))
            # Indication of Node + paired Memory Slot
            if inspected_linked_list.nodes[current_node].get_value()==value: # Found the node searched for.
                self.scene.play(AnimationGroup(
                                Indicate(inspected_linked_list.nodes[current_node],
                                         scale_factor=2,color=PURE_GREEN)),
                                Indicate(self.memory.slots[self.find_memory_index(inspected_linked_list.nodes[current_node].get_value())],
                                         scale_factor=2.0,color=PURE_GREEN)
                    )
                searching = False
            else:
                self.scene.play(AnimationGroup(
                                Indicate(inspected_linked_list.nodes[current_node],
                                         scale_factor=1.2,color=WHITE)),
                                Indicate(self.memory.slots[self.find_memory_index(inspected_linked_list.nodes[current_node].get_value())],
                                         scale_factor=1.2,color=WHITE))
                current_node+=1
        # If searching = True : Value was not found
        # If searching = False: Value was found
        if searching:
            return False
        else:
            return True
        
    def add_value(self,value):
        found = self.search(value)
        if not found:
            hash = self.hash_table.custom_hash(value, bucket_size = len(self.hash_table.array.slots))
    
            # Triggering a resizing
            if self.hash_table.linked_lists[hash].get_length()>=self.hash_table.max_ll_length and self.hash_table.resizing:
                # Resizing code
                # Recording old occupied memory slots
                old_occupied_memory_slots = [] 
                old_occupied_memory_slots.extend(self.ht_array) #why are we doing this?
                                                                # Keeping track of what slots are a part of the
                                                                # old hash table.
                for pair in self.pairs:
                    old_occupied_memory_slots.append(pair[1])
                # Changing color of the old array + its memory slots to yellow.
                if not self.color_coding:
                    self.hash_table.turn_yellow()
                    self.memory.set_multiple_slot_color(old_occupied_memory_slots,YELLOW)
                else:
                    self.hash_table.turn_grey()
                    self.memory.set_multiple_slot_color(old_occupied_memory_slots,GREY)
                # Scale down orginal hash table (+ recolor)
                self.hash_table.resizing_setup()
                self.hash_table.shrink_old_hash_table()

                # Initialize new array (Memory + regular)
                # Hash table
                self.hash_table.create_new_hash_table(doubling=True)
                old_ht_array = self.ht_array

                if self.color_coding:
                    #assign colors to resized HT slots in order from available_colors
                    for i in enumerate(self.hash_table.array.slots):
                        self.hash_table.array.slots[i[0]].set_color(self.available_colors[i[0]])
                # Memory
                self.ht_array = self.memory.select_random_slots(len(self.ht_array)*2)
                if self.color_coding:
                    self.memory.set_multiple_slot_state(self.ht_array,1,self.available_colors)
                else:
                    self.memory.set_multiple_slot_state(self.ht_array,1)
                # Rehashing (read copy) values from 
                for i in range(len(self.hash_table.old_array.slots)):
                    # Indicating array slots in HT + Memory.
                    self.scene.play(AnimationGroup(
                                    Indicate(self.memory.slots[old_ht_array[i]], color=WHITE),
                                    Indicate(self.hash_table.old_array.slots[i],color=WHITE)))
                    # Looping through LL.
                    for k in range(len(self.hash_table.old_linked_lists[i].nodes)):
                        node = self.hash_table.old_linked_lists[i].nodes[k]
                        node_value = node.get_value()
                        slot_index = self.find_memory_index(node_value)
                        self.scene.play(AnimationGroup(
                            Indicate(node),
                            Indicate(self.memory.slots[slot_index],color=WHITE)))
                        self.regular_add(node_value) #error here at adding 
                # Fade out old memory + old array
                self.hash_table.fade_out_old_hash_table()
                self.memory.set_multiple_slot_state(old_occupied_memory_slots,0)
                

                self.regular_add(value)
            # No resizing
            else:
                self.regular_add(value)
    
    
    def regular_add(self,value):
        self.hash_table.add_value(value)
        i = self.memory.add_value()
        pair = [value,i]
        self.pairs.append(pair)
        
        if self.color_coding:
            
            #new memory slot has same colour of the HT slot at position hash
            hash = self.hash_table.custom_hash(value, len(self.hash_table.array.slots))
            self.memory.set_slot_state(i,1,self.available_colors[hash])
        
    def remove_value(self,value):
        found = self.search(value)
        if found:
            index_to_remove = self.find_memory_index(value)
            self.pairs.remove([value,index_to_remove])
            hash = self.hash_table.custom_hash(value, bucket_size = len(self.ht_array))
            self.hash_table.linked_lists[hash].remove_value_no_search(value)
            self.memory.remove_value(index_to_remove)

    def find_memory_index(self,value):
        for pair in self.pairs:
            if pair[0] == value:
                return pair[1]
    
        
        

        
        

from manim import *
from DataStructures.ResizingArray import ResizingArray

class HashTableLinearProbing(ResizingArray):
        def __init__(self, scene:Scene,
                     side_length:float=2.0,
                     size:int =4,
                     **kwargs):
            super().__init__(scene = scene,size=size,side_length=side_length,**kwargs)
            self.size = size

        def custom_hash(self,char,bucket_size):
            if 'a' <= char <= 'z':
                return (ord(char) - ord('a')) % bucket_size
            else:
                raise ValueError("Input must be a lowercase letter from 'a' to 'z'")
            
        def regular_insert(self,value):
             index = self.custom_hash(value,bucket_size=len(self.array.slots))
             b = True
             # Create value above original index
             value_text_temp = Text(value).scale(self.array.slots[0].square.height).move_to(self.array.slots[index].square.get_center()).shift(self.array.slots[index].square.height*UP)
             self.scene.play(Create(value_text_temp))
             while b:
                  if self.array.get_value(index) is None: # Inserting into original index
                       b=False
                       self.scene.play(value_text_temp.animate.shift(self.array.slots[index].square.height*DOWN))
                       self.array.write(label=index,value=value)
                       self.scene.remove(value_text_temp)
                       self.filled+=1
                  else:
                    self.scene.play(value_text_temp.animate.shift(0.35*self.array.slots[index].square.height*DOWN))
                    self.scene.play(value_text_temp.animate.shift(0.35*self.array.slots[index].square.height*UP))
                    index+=1
                    if index==len(self.array.slots):
                        index=0
                    self.scene.play(value_text_temp.animate.move_to(self.array.slots[index].square.get_center()+[0,self.array.slots[index].square.height,0]))


        def insert(self,value):
            if self.is_full():
                self.scene.play(self.array.animate.to_edge(UP,buff=0.5))
                self.instantiate_resized_array(doubling=True)
                self.move_old_array_into_place_for_replacement()
                self.create_new_array_on_screen()
                self.copy_to_new_array()
                self.replace_old_array_with_new()
                self.regular_insert(value)
            else:
                self.regular_insert(value)

        def delete(self,value):
            if self.needs_decrease():
                self.scene.play(self.array.animate.to_edge(UP,buff=0.5))
                self.instantiate_resized_array(doubling=False)
                self.move_old_array_into_place_for_replacement()
                self.create_new_array_on_screen()
                self.copy_to_new_array()
                self.replace_old_array_with_new()
                self.scene.play(self.regular_delete(value))
            else:
                delete_animation = self.regular_delete(value)
                if delete_animation is not None:
                    self.scene.play(delete_animation)

        def regular_delete(self,value):
            index = self.custom_hash(value,bucket_size=len(self.array.slots))
            b = True
            counter = 0
            while b:
                if self.array.get_value(index)==value:
                    b=False
                    self.filled -=1
                    return self.array.delete(index)
                index+=1
                #Making sure it doesn't loop forever if the value is not in the hash table.
                counter+=1
                if counter>=len(self.array.slots):
                    b=False

        def copy_to_new_array(self):
            for i in range(self.array.size):
                if self.array.has_value(i):
                    value = self.array.get_value(i) # The value is the slot.
                    hash_index_new_array = self.custom_hash(value,bucket_size=len(self.new_array.slots))
                    original_slot_copy = self.array.create_slot_copy(i) # Copy of slot in original array
                    new_slot_copy = self.new_array_temporary.create_slot_copy(hash_index_new_array,new_value=self.array.slots[i].get_value())
                    # Below adds indication pr. slot before copying. (We may or may not want it).
                    self.indicate_slot(self.array.slots[i])
                    self.scene.add(original_slot_copy) # Adding copy to the scene.
                    # End of Indication animation.

                    # The slot with the index is available
                    if self.new_array.get_value(hash_index_new_array) is None:
                        self.scene.play(AnimationGroup(
                            original_slot_copy.animate.move_to(self.new_array_temporary.slots[hash_index_new_array].get_center()),
                            Transform(original_slot_copy,new_slot_copy)
                        ))
                        self.new_array.slots[hash_index_new_array].set_value(self.array.slots[i].get_value())
                        self.new_array_temporary.slots[hash_index_new_array].set_value(self.array.slots[i].get_value())
                        self.scene.remove(original_slot_copy)
                    # The slot with the index is NOT available
                    else:
                        self.scene.play(original_slot_copy.animate.move_to(self.new_array_temporary.slots[hash_index_new_array].get_center()+[0,self.new_array_temporary.slots[hash_index_new_array].square.height*1.2,0]))
                        self.scene.play(original_slot_copy.animate.shift(self.new_array_temporary.slots[hash_index_new_array].square.height*0.2*DOWN))
                        self.scene.play(original_slot_copy.animate.shift(self.new_array_temporary.slots[hash_index_new_array].square.height*0.2*UP))
                        b=True
                        while b:
                            hash_index_new_array+=1
                            if hash_index_new_array==len(self.new_array.slots):
                                hash_index_new_array=0
                            self.scene.play(original_slot_copy.animate.move_to(self.new_array_temporary.slots[hash_index_new_array].get_center()+[0,self.new_array_temporary.slots[hash_index_new_array].square.height*1.2,0]))
                            #Place found
                            if self.new_array.get_value(hash_index_new_array) is None:
                                new_slot_copy = self.new_array_temporary.create_slot_copy(hash_index_new_array,new_value=self.array.slots[i].get_value())
                                self.scene.play(AnimationGroup(
                                    original_slot_copy.animate.move_to(self.new_array_temporary.slots[hash_index_new_array].get_center()),
                                    Transform(original_slot_copy,new_slot_copy)
                                    ))
                                b=False
                            #Place NOT found
                            else:
                                self.scene.play(original_slot_copy.animate.shift(self.new_array_temporary.slots[hash_index_new_array].square.height*0.2*DOWN))
                                self.scene.play(original_slot_copy.animate.shift(self.new_array_temporary.slots[hash_index_new_array].square.height*0.2*UP))
                        self.new_array.slots[hash_index_new_array].set_value(self.array.slots[i].get_value())
                        self.new_array_temporary.slots[hash_index_new_array].set_value(self.array.slots[i].get_value())
                        self.scene.remove(original_slot_copy)


            

from typing import List, Union, Dict
from collections import Counter

def create_backwards_dict(forward, prefix=''):
    backwards = {}
    for key, value in forward.items():
        current_key = prefix + str(key)
        if type(value) != dict:
            backwards[value] = current_key
        else:
            backwards.update(
                create_backwards_dict(value, prefix=current_key)
            )
    return backwards

def flatten_dict(d, prefix=''):
    flatten = {}
    for key, value in d.items():
        current_key = prefix + str(key)
        if type(value) != dict:
            flatten[current_key] = value
        else:
            flatten.update(
                flatten_dict(value, prefix=current_key)
            )
    return flatten

class Huffman():
    """
    Huffman receives list of int and returns a 0-1 dict
    The dict mapping the Huffman code to the original int numbers
    """
    def __init__(self, numbers: List[int]):
        self._numbers = numbers
    
    def build_huffman_dict(self) -> Dict[int, Union[Dict, int]]:
        items_hierarchy = self.build_items_hierarchy(self._numbers)
        return self.unpack_items_hierarchy_to_dict(items_hierarchy)
    
    @staticmethod
    def _lst_index(lst, item):
        for index, lst_item in enumerate(lst):
            if item == lst_item:
                return index
        return -1


    @staticmethod
    def _list_replace(lst, old, new):
        for i in range(len(lst)):
            index = Huffman._lst_index(old, lst[i])
            if index >= 0:
                lst[i] = new[index]

    @staticmethod
    def build_items_hierarchy(items):
        items_hierarchy = items.copy()
        counter = Counter(items_hierarchy)
        most_common = counter.most_common()
        while len(most_common) > 1:
            # Get the 2 least common numbers together
            combined_items = (most_common[-1][0], most_common[-2][0])
            Huffman._list_replace(
                items_hierarchy, [most_common[-1][0], most_common[-2][0]], [combined_items, combined_items]
            )
            # Build the most_common hierarchy again after switching the 2 least common by 1
            counter = Counter(items_hierarchy)
            most_common = counter.most_common()
        return items_hierarchy[0]
        
    @staticmethod
    def unpack_items_hierarchy_to_dict(items_hierarchy) -> Dict[int, Union[Dict, int]]:
        # Build the final dict by the final items hierarcy
        if type(items_hierarchy) != tuple:
            return items_hierarchy
        
        zero, one = items_hierarchy
        return {
            0: Huffman.unpack_items_hierarchy_to_dict(zero),
            1: Huffman.unpack_items_hierarchy_to_dict(one)
        }

def test():
    huffman = Huffman([1,2,3,1,1,1,1,2,2,1,1,3])
    print(huffman.build_huffman_dict())

if __name__ == '__main__':
    test()

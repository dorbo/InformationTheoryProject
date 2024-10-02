from typing import List, Tuple
from logger import logger

class LZ77():
    """
    LZ77 (Lempel Ziv 77) receives data and returns a list of tuples
    In each tuple:
    - shift - from where to copy the bytes from the current location
    - length - how much bytes to copy
    """
    LATIN1_BYTES = bytearray(list(range(256)))
    CACHE_MAX_LENGTH = 5
    def __init__(self, data: bytes) -> None:
        self._data: bytes = self.LATIN1_BYTES + data
        self._mapping_size = (len(self._data) // 10)
        self._mapping: List[Tuple[int, int]] = [None] * self._mapping_size
        self._mapping_index = 0
        self._semi_cache = {}
    
    def find_semi_cache(self, search_str, position, length):
        """
        Use cache for the bytes sequence searching for sequences with max length of 
        """
        search_str = bytes(search_str)
        if search_str in self._semi_cache:
            return self._semi_cache[search_str]
        # Use rfind in order to find the nearest sequence of bytes to copy (lowest shift)
        if length > 5:
            result = self._data.rfind(search_str, position - length - 2048, position - length)
        else:
            result = self._data.rfind(search_str, 0, position - length)
        if result > 0:
            # Save to cache only if found (Otherwise it might be found later with later position)
            self._semi_cache[search_str] = result
        return result

    def find_best_copy(self, position) -> Tuple[int, int]:
        best_start, max_length = None, 0
        max_possible_length = len(self._data) - position
        
        length = 1
        result = self.find_semi_cache(self._data[position:position + length], position, length)
        while result > 0 and length <= max_possible_length:
            max_length = length
            best_start = result
            length += 1
            result = self.find_semi_cache(self._data[position:position + length], position, length)
        return best_start, max_length
    
    def mapping_append(self, value):
        """
        Use preallocated mapping for the mapping
        _mapping is growing by 1 inside a long for loop
        growing will take a lot of runtime - allocating new list with length+1, than copy O(n)
        with pre allocation - accessing each element with O(1), and reallocating
        """
        if self._mapping_index >= self._mapping_size:
            logger.debug('Resize Mapping')
            expand_by = self._mapping_size // 10
            self._mapping += [None] * expand_by
            self._mapping_size += expand_by
        self._mapping[self._mapping_index] = value
        self._mapping_index += 1
    
    def clear_mapping_none(self):
        # Clear the extra allocated mapping list items
        self._mapping = self._mapping[:self._mapping_index]

    def compress(self):
        position = 256
        while position < len(self._data):
            start, length = self.find_best_copy(position)
            self.mapping_append((position - start, length))
            position += length
        self.clear_mapping_none()
        return self._mapping

def test():
    lz = LZ77(b'aeacdaecdaecd')
    print(lz.compress())

if __name__ == '__main__':
    test()

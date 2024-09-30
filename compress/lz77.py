import time
from typing import List, Tuple
from logger import logger

class LZ77():
    LATIN1_BYTES = bytearray(list(range(256)))
    def __init__(self, data: bytes) -> None:
        self._data: bytes = self.LATIN1_BYTES + data
        self._mapping_size = (len(self._data) // 10)
        self._mapping: List[Tuple[int, int]] = [None] * self._mapping_size
        self._mapping_index = 0
        self._semi_cache = {}
    
    def search_from(self, start, position):
        length = 0
        while start + length < len(self._data) and \
            position + length < len(self._data) and \
            self._data[start + length] == self._data[position + length]:
            length += 1
        length = min(length, position - start)
        return start, length
    
    def find_best_copy(self, position) -> Tuple[int, int]:
        best_start, max_length = None, 0
        for i in range(position):
            start, length = self.search_from(position - i - 1, position)
            if length > max_length:
                max_length = length
                best_start = start
        return best_start, max_length
    
    def find_semi_cache(self, search_str, position, length):
        search_str = bytes(search_str)
        if search_str in self._semi_cache:
            return self._semi_cache[search_str]
        if length > 5:
            result = self._data.rfind(search_str, position - length - 2048, position - length)
        else:
            result = self._data.rfind(search_str, 0, position - length)
        if result > 0:
            # Save to cache only if found (Otherwise it might be found later with later position)
            self._semi_cache[search_str] = result
        return result

    def find_best_copy2(self, position) -> Tuple[int, int]:
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
        if self._mapping_index >= self._mapping_size:
            print('Resize Mapping')
            expand_by = self._mapping_size // 10
            self._mapping += [None] * expand_by
            self._mapping_size += expand_by
        self._mapping[self._mapping_index] = value
        self._mapping_index += 1
    
    def clear_mapping_none(self):
        self._mapping = self._mapping[:self._mapping_index]

    def compress(self):
        position = 256
        while position < len(self._data):
            start, length = self.find_best_copy2(position)
            if length > 35: #position > 100000 and position % 10000 < 10:
                logger.debug(f'position {position} length {length} index {self._mapping_index}')
            self.mapping_append((position - start, length))
            position += length
        self.clear_mapping_none()
        return self._mapping

def test():
    lz = LZ77(b'aeacdaecdaecd')
    print(lz.compress())

if __name__ == '__main__':
    test()

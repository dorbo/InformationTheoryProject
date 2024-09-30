import math
from bytes_utils import iterate_bits

class RLE():
    def __init__(self):
        self._number = None
    
    @staticmethod
    def _number_to_bytes(number: int):
        bits_needed = math.floor(math.log(number, 2)) + 1
        bytes_needed = math.ceil(bits_needed / 8)
        return number.to_bytes(bytes_needed, 'big')
    
    @staticmethod
    def _number_with_ones_bits(amount_of_ones: int):
        return 2*sum([2 ** i for i in range(amount_of_ones)])
    
    @staticmethod
    def _rle_bits_prefix(number_len: int):
        bytes_needed_bits = RLE._number_with_ones_bits(number_len)
        return RLE._number_to_bytes(bytes_needed_bits)

    def rle_write(self, number):
        self._number = number
        number_in_bytes = self._number_to_bytes(self._number)
        bits_prefix = self._rle_bits_prefix(len(number_in_bytes))
        return bits_prefix + number_in_bytes
    
    def rle_read(self, bytes):
        position = 0        
        number_bytes_length = 0
        first_one_seen = False
        finish_reading = False
        for byte in bytes:
            for bit in iterate_bits(byte):
                if bit == 0:
                    if first_one_seen:
                        finish_reading = True
                    continue
                if bit == 1:
                    first_one_seen = True
                    number_bytes_length += 1
            position += 1
            if finish_reading:
                break
        self._number = int.from_bytes(bytes[position:position + number_bytes_length], 'big')
        position += number_bytes_length
        return position



def test_write():
    rle = RLE()
    print(rle.rle_write(300))

def test_read():
    rle = RLE()
    print(rle.rle_read(b'\x06\x01,'))
    print(rle._number)

if __name__ == '__main__':
    test_read()

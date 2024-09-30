import json
from rle import RLE
from lz77 import LZ77
from huffman import flatten_dict
from bytes_utils import iterate_bits

rle = RLE()

def decode_huffman_dict(dict_bytes):
    return json.loads(dict_bytes.decode('latin1'))

def get_lz77_pairs(compressed_data, flatten_shift, flatten_length):
    lz77_pairs = []
    current_key = ''
    shift, length = None, None
    for bit in iterate_bits(compressed_data):
        current_key += str(bit)
        if shift is None:
            if current_key in flatten_shift:
                shift = flatten_shift[current_key]
                current_key = ''
        else:
            if current_key in flatten_length:
                length = flatten_length[current_key]
                current_key = ''
        if shift is not None and length is not None:
            lz77_pairs.append((shift, length))
            shift, length = None, None
    return lz77_pairs

def reconstruct_data(compressed_data, flatten_shift, flatten_length, len_mapping):
    data = LZ77.LATIN1_BYTES.copy()
    position = len(data)
    lz77_pairs = get_lz77_pairs(compressed_data[position:], flatten_shift, flatten_length)
    for shift, length in lz77_pairs[:len_mapping]:
        a = data[position - shift : position - shift + length]
        data += data[position - shift : position - shift + length]
        position += length
        print(data[len(LZ77.LATIN1_BYTES):])
    return data[len(LZ77.LATIN1_BYTES):]

def decompress(data):
    position = rle.rle_read(data)
    shift_huffman_rle_len = rle._number
    shift_huffman_bytes = data[position:position + shift_huffman_rle_len]
    shift_huffman_dict = decode_huffman_dict(shift_huffman_bytes)
    flatten_shift = flatten_dict(shift_huffman_dict)
    position += shift_huffman_rle_len

    position += rle.rle_read(data[position:])
    length_huffman_rle_len = rle._number
    length_huffman_bytes = data[position:position + length_huffman_rle_len]
    length_huffman_dict = decode_huffman_dict(length_huffman_bytes)
    flatten_length = flatten_dict(length_huffman_dict)
    position += length_huffman_rle_len

    position += rle.rle_read(data[position:])
    len_mapping = rle._number

    return reconstruct_data(data[position:], flatten_shift, flatten_length, len_mapping)

def test():
    with open('compressed_test.cm', 'rb') as f:
        data = f.read()
    print(decompress(data))

if __name__ == '__main__':
    test()

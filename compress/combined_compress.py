import json

from logger import logger
from lz77 import LZ77
from huffman import Huffman, create_backwards_dict
from rle import RLE


def get_lz_shift_length_mapping(data):
    lz = LZ77(data)
    mapping = lz.compress()
    shift_mapping = [mapped[0] for mapped in mapping]
    length_mapping = [mapped[1] for mapped in mapping]
    return shift_mapping, length_mapping

def get_huffman_dict(numbers_list):
    huffman = Huffman(numbers_list)
    return huffman.build_huffman_dict()

def get_bytes_huffman_dict(d):
    return json.dumps(d).encode('latin1')

def get_rle(number):
    rle = RLE()
    return rle.rle_write(number)

def convert_zero_one_str_to_bytes(string):
    converted = bytes(int(string[i:i+8], 2) for i in range(0, len(string), 8))
    end = string[8 * (len(converted) - 1):]
    padding = (8 - len(end)) * '0'
    # padding from the *right* the last byte
    last_byte_str = end + padding
    last_byte = int(last_byte_str, 2).to_bytes(1, 'big')
    converted = converted[:-1] + last_byte
    return converted

def create_lz_mapping_using_huffman(shift_mapping, length_mapping, shift_huffman, length_huffman):
    shift_huffman_backwards = create_backwards_dict(shift_huffman)
    length_huffman_backwards = create_backwards_dict(length_huffman)

    lz_mapping = ''
    for shift, length in zip(shift_mapping, length_mapping):
        lz_mapping += shift_huffman_backwards[shift] + length_huffman_backwards[length]
    return convert_zero_one_str_to_bytes(lz_mapping)

def compress(data):
    logger.info('Start Compressing')
    logger.info(f'Data len: {len(data)}')
    
    logger.debug('Mapping LZ77 Started')
    shift_mapping, length_mapping = get_lz_shift_length_mapping(data)
    logger.debug('Mapping LZ77 Completed')
    
    logger.debug(f'Len mapping RLE ({len(shift_mapping)})')
    len_mapping_bytes = get_rle(len(shift_mapping))
    logger.debug('Len mapping RLE Completed')

    logger.debug('Huffman Dict - Shift')
    shift_huffman = get_huffman_dict(shift_mapping)
    shift_huffman_bytes = get_bytes_huffman_dict(shift_huffman)
    shift_huffman_rle_len = get_rle(len(shift_huffman_bytes))
    logger.debug('Huffman Dict - Shift Completed')

    logger.debug('Huffman Dict - Length')
    length_huffman = get_huffman_dict(length_mapping)
    length_huffman_bytes = get_bytes_huffman_dict(length_huffman)
    length_huffman_rle_len = get_rle(len(length_huffman_bytes))
    logger.debug('Huffman Dict - Length Completed')

    lz_mapping_using_huffman = create_lz_mapping_using_huffman(shift_mapping, length_mapping, shift_huffman, length_huffman)

    logger.debug('Concat results')
    result = b''.join([
        shift_huffman_rle_len,
        shift_huffman_bytes,
        length_huffman_rle_len,
        length_huffman_bytes,
        len_mapping_bytes,
        LZ77.LATIN1_BYTES,
        lz_mapping_using_huffman,
    ])
    logger.debug('Concat results completed')
    return result


def test():
    with open('compressed_test.cm', 'wb') as f:
        f.write(compress(b'aeacdaecdaecd'))

def compress_dickens():
    with open('dickens.txt', 'rb') as f:
        data = f.read()
    with open('compressed.cm', 'wb') as f:
        f.write(compress(data))

if __name__ == '__main__':
    compress_dickens()
    # test()

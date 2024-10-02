import argparse

from combined_compress import compress
from combined_decompress import decompress

COMPRESSED_SUFFIX = '.cm'

def compress_file(file_name):
    compressed_file_name = f'{file_name}{COMPRESSED_SUFFIX}'
    with open(file_name, 'rb') as f:
            data = f.read()
    with open(compressed_file_name, 'wb') as f:
        f.write(compress(data))
    return compressed_file_name

def decompress_file(file_name):
    decompressed_file_name = file_name[:-len(COMPRESSED_SUFFIX)]
    with open(file_name, 'rb') as f:
        data = f.read()
    with open(decompressed_file_name, 'wb') as f:
        f.write(decompress(data))
    return decompressed_file_name

def main(filename, decompress):
    if not decompress:
        output = compress_file(filename) 
    else:
        output = decompress_file(filename)
    print(f'Output at: {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='compress project',
        description='The program compresses and decompresses files',
    )
    parser.add_argument('filename')
    parser.add_argument('-d', '--decompress', action='store_true')
    args = parser.parse_args()
    main(args.filename, args.decompress)

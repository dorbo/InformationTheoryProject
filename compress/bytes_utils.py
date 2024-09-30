def iterate_bits(bytes):
    if type(bytes) == int:
        bytes = [bytes]
    for byte in bytes:
        for bit in format(byte, '08b'):
            yield int(bit)

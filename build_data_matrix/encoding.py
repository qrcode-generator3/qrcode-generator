from build_data_matrix.qr_Structure import DATA_CODEWORDS_TABLE


NUMERIC_MODE = 1
ALPHANUMERIC_MODE = 2
BYTE_MODE = 4
KANJI_MODE = 8


# example table for version 1 - 9
CHAR_COUNT_BITS = {
    (1, 9):   {NUMERIC_MODE: 10, ALPHANUMERIC_MODE: 9,  BYTE_MODE: 8,  KANJI_MODE: 8},
    (10, 26): {NUMERIC_MODE: 12, ALPHANUMERIC_MODE: 11, BYTE_MODE: 16, KANJI_MODE: 10},
    (27, 40): {NUMERIC_MODE: 14, ALPHANUMERIC_MODE: 13, BYTE_MODE: 16, KANJI_MODE: 12},
}

ALPHANUMERIC_CHARS = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")


def get_char_count_bits(version: int, mode: int) -> int:
    for (low, high), bits in CHAR_COUNT_BITS.items():
        if low <= version <= high:
            return bits[mode]
    raise ValueError("Invalid version")


def identify_encoding(data: str) -> int:
    if data.isdigit():
        return NUMERIC_MODE
    
    if all(c in ALPHANUMERIC_CHARS for c in data):
        return ALPHANUMERIC_MODE
    
    # include kanji encoding
    
    return BYTE_MODE


def encode_data(bits: list[int], data: str, encoding: int):
    if encoding == NUMERIC_MODE:
        pass

    if encoding == ALPHANUMERIC_MODE:
        pass

    if encoding == BYTE_MODE:
        encode_byte(bits=bits, data=data)

    if encoding == KANJI_MODE:
        pass



def encode_byte(bits: list[int], data: str):
    for byt in data.encode("iso-8859-1"):
        append_bits(bits=bits, value=byt, length=8)


def append_bits(bits: list[int], value: int, length: int):
    for i in reversed(range(length)):
        bits.append((value >> i) & 1)


def build_bit_stream(data: str, encoding: int, version: int, ec_level: str) -> list[int]:
    '''
    The bit format looks like this

    [ MODE ][ CHAR COUNT ][ DATA ][ TERMINATOR ][ BYTE PAD ][ PAD BYTES ]
    '''
    bits: list[int] = []

    # add mode bits
    append_bits(bits=bits, value=encoding, length=4)

    # add character count bits
    count_bits = get_char_count_bits(version, encoding)
    append_bits(bits, len(data), count_bits)

    # add data bits
    encode_data(bits=bits, data=data, encoding=encoding)

    # add terminator bits
    max_capacity = DATA_CODEWORDS_TABLE[version][ec_level] * 8
    remaining = max_capacity - len(bits)


    terminator_length = min(4, remaining)
    bits.extend([0] * terminator_length)


    # add pad for byte boundary
    while len(bits) % 8 != 0:
        bits.append(0)

    
    # add pad byte
    i = 0
    while len(bits) < max_capacity:
        append_bits(bits, [0xEC, 0x11][i % 2], 8)
        i += 1


    return bits


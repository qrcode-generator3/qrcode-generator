from reedsolo import RSCodec

from build_data_matrix.ec_blocks_table import EC_BLOCKS_TABLE


def bits_to_codewords(bit_stream: list[int]) -> list[int]:
    code_words = []

    for i in range(0, len(bit_stream), 8):
        byte = 0

        for bit in bit_stream[i:i+8]:
            byte = (byte << 1) | bit
        
        code_words.append(byte)
    
    return code_words


def split_into_blocks(codewords, version, ec_level):
    info = EC_BLOCKS_TABLE[(version, ec_level)]
    blocks = []

    index = 0
    for size in info["data"]:
        blocks.append(codewords[index:index + size])
        index += size

    return blocks



def generate_ec_codewords(block, ec_count):
    rsc = RSCodec(nsym=ec_count, fcr=0, generator=2, prim=0x11d)
    
    # We want the remainder (the parity bytes)
    encoded = rsc.encode(bytearray(block))
    return list(encoded[-ec_count:])


def generate_all_ec_blocks(blocks, version, ec_level):
    info = EC_BLOCKS_TABLE[(version, ec_level)]
    ec_count = info["ec"]

    ec_blocks = []
    for block in blocks:
        ec_blocks.append(generate_ec_codewords(block, ec_count))

    return ec_blocks


def interleave_blocks(blocks):
    result = []
    max_len = max(len(block) for block in blocks)

    for i in range(max_len):
        for block in blocks:
            if i < len(block):
                result.append(block[i])

    return result


def interleave_ec_blocks(ec_blocks):
    result = []
    ec_len = len(ec_blocks[0])

    for i in range(ec_len):
        for block in ec_blocks:
            result.append(block[i])

    return result


def build_final_codewords(bit_stream, version, ec_level):
    codewords = bits_to_codewords(bit_stream)
    blocks = split_into_blocks(codewords, version, ec_level)
    ec_blocks = generate_all_ec_blocks(blocks, version, ec_level)

    data_interleaved = interleave_blocks(blocks)
    ec_interleaved = interleave_ec_blocks(ec_blocks)

    return data_interleaved + ec_interleaved

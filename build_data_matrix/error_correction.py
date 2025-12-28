# Custom Reed-Solomon implementation (GF(256))
def gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    # Log/Antilog based multiplication
    # Precomputed tables for speed/simplicity
    log = [0] * 256
    exp = [0] * 512
    x = 1
    for i in range(255):
        exp[i] = x
        exp[i + 255] = x
        log[x] = i
        x = (x << 1) ^ (0x11d if x & 0x80 else 0)
    
    return exp[log[a] + log[b]]

def gf_poly_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for j in range(len(q)):
        for i in range(len(p)):
            r[i + j] ^= gf_mul(p[i], q[j])
    return r

def rs_generator_poly(nsym):
    g = [1]
    # QR code uses alpha^0 = 1, alpha^1 = 2, ...
    # generator polynomial: (x - alpha^0)(x - alpha^1)...(x - alpha^(nsym-1))
    # In GF(256), subtraction is same as XOR.
    # alpha^i is 2^i if we use the same generator as reedsolo
    
    exp = [0] * 512
    x = 1
    for i in range(255):
        exp[i] = x
        exp[i + 255] = x
        x = (x << 1) ^ (0x11d if x & 0x80 else 0)

    for i in range(nsym):
        # Multiply g by (x + alpha^i)
        g = gf_poly_mul(g, [1, exp[i]])
    return g

def rs_encode(data, nsym):
    gen = rs_generator_poly(nsym)
    # Division of data by gen
    res = list(data) + [0] * nsym
    
    # Precompute tables for speed
    log = [0] * 256
    exp = [0] * 512
    x = 1
    for i in range(255):
        exp[i] = x
        exp[i + 255] = x
        log[x] = i
        x = (x << 1) ^ (0x11d if x & 0x80 else 0)

    for i in range(len(data)):
        coef = res[i]
        if coef != 0:
            log_coef = log[coef]
            for j in range(1, len(gen)):
                if gen[j] != 0:
                    res[i + j] ^= exp[log_coef + log[gen[j]]]
    
    return res[len(data):]

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
    return rs_encode(block, ec_count)


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

from build_data_matrix.matrix.matrix import create_matrix
from build_data_matrix.matrix.pattern import place_alignments, place_dark_module, place_finders, place_timing
from build_data_matrix.matrix.constant import VERSION_INFO


def place_data(matrix, reserved, codewords):
    size = len(matrix)

    bits = []
    for cw in codewords:
        for i in range(7, -1, -1):
            bits.append((cw >> i) & 1)

    idx = 0
    direction = -1
    col = size - 1

    while col > 0:
        if col == 6:
            col -= 1

        row_range = range(size-1, -1, -1) if direction == -1 else range(size)

        for row in row_range:
            for c in [col, col-1]:
                if reserved[row][c]:
                    continue
                if idx < len(bits):
                    matrix[row][c] = bits[idx]
                    idx += 1
                else:
                    matrix[row][c] = 0

        col -= 2
        direction *= -1

def reserve_format_areas(reserved):
    size = len(reserved)

    # Top-left format
    for i in range(9):
        if i != 6:
            reserved[8][i] = True
            reserved[i][8] = True

    # Top-right format
    for i in range(8):
        reserved[8][size - 1 - i] = True

    # Bottom-left format
    for i in range(7):
        reserved[size - 1 - i][8] = True

def reserve_version_areas(reserved, version):
    if version < 7:
        return
    size = len(reserved)
    # Bottom-left and top-right areas (6x3 each)
    for i in range(6):
        for j in range(3):
            reserved[size - 11 + i][j] = True
            reserved[j][size - 11 + i] = True

def place_version_info(matrix, version):
    if version < 7:
        return
    size = len(matrix)
    info = VERSION_INFO.get(version)
    if info is None:
        return

    for i in range(18):
        bit = (info >> i) & 1
        # Bottom-left: 6x3 block
        matrix[size - 11 + (i % 6)][i // 6] = bit
        # Top-right: 3x6 block (transpose)
        matrix[i // 6][size - 11 + (i % 6)] = bit

def build_base_matrix(version, final_codewords):
    matrix, reserved = create_matrix(version)

    place_finders(matrix, reserved)
    place_timing(matrix, reserved)
    place_alignments(matrix, reserved, version)
    place_dark_module(matrix, reserved, version)
    reserve_format_areas(reserved)
    reserve_version_areas(reserved, version)
    
    place_version_info(matrix, version)
    place_data(matrix, reserved, final_codewords)

    return matrix, reserved

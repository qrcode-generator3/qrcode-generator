from build_data_matrix.matrix.constant import ALIGNMENT_POSITIONS


def place_finder(matrix, reserved, top, left):
    pattern = [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1],
    ]

    for r in range(7):
        for c in range(7):
            matrix[top + r][left + c] = pattern[r][c]
            reserved[top + r][left + c] = True


def place_separator(matrix, reserved, top, left):
    for i in range(-1, 8):
        for j in [-1, 7]:
            if 0 <= top+i < len(matrix) and 0 <= left+j < len(matrix):
                matrix[top+i][left+j] = 0
                reserved[top+i][left+j] = True

        for j in [-1, 7]:
            if 0 <= top+j < len(matrix) and 0 <= left+i < len(matrix):
                matrix[top+j][left+i] = 0
                reserved[top+j][left+i] = True


def place_finders(matrix, reserved):
    size = len(matrix)

    positions = [
        (0, 0),
        (0, size - 7),
        (size - 7, 0),
    ]

    for r, c in positions:
        place_finder(matrix, reserved, r, c)
        place_separator(matrix, reserved, r, c)


def place_timing(matrix, reserved):
    size = len(matrix)

    for i in range(8, size - 8):
        val = (i % 2)
        if not reserved[6][i]:
            matrix[6][i] = 1 - val
            reserved[6][i] = True

        if not reserved[i][6]:
            matrix[i][6] = 1 - val
            reserved[i][6] = True


def place_alignment(matrix, reserved, row, col):
    pattern = [
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
    ]

    for r in range(5):
        for c in range(5):
            matrix[row-2+r][col-2+c] = pattern[r][c]
            reserved[row-2+r][col-2+c] = True


def place_alignments(matrix, reserved, version):
    positions = ALIGNMENT_POSITIONS.get(version, [])

    for r in positions:
        for c in positions:
            if reserved[r][c]:
                continue
            place_alignment(matrix, reserved, r, c)




def place_dark_module(matrix, reserved, version):
    size = len(matrix)
    row = 4 * version + 9
    col = 8

    matrix[row][col] = 1
    reserved[row][col] = True


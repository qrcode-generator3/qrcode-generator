
def apply_mask(matrix, reserved, mask):
    size = len(matrix)
    masked = [row[:] for row in matrix]

    for r in range(size):
        for c in range(size):
            if reserved[r][c]:
                continue  # skip function patterns

            invert = False
            if mask == 0: invert = (r + c) % 2 == 0
            elif mask == 1: invert = r % 2 == 0
            elif mask == 2: invert = c % 3 == 0
            elif mask == 3: invert = (r + c) % 3 == 0
            elif mask == 4: invert = (r//2 + c//3) % 2 == 0
            elif mask == 5: invert = (r*c) % 2 + (r*c) % 3 == 0
            elif mask == 6: invert = ((r*c) % 2 + (r*c) % 3) % 2 == 0
            elif mask == 7: invert = ((r + c) % 2 + (r*c) % 3) % 2 == 0

            if invert:
                masked[r][c] ^= 1  # flip 0↔1

    return masked



def penalty_score(matrix):
    size = len(matrix)
    score = 0

    # Rule 1: consecutive same-color modules in rows
    for r in range(size):
        count = 1
        last = matrix[r][0]
        for c in range(1, size):
            if matrix[r][c] == last:
                count += 1
            else:
                if count >= 5: score += 3 + (count - 5)
                count = 1
                last = matrix[r][c]
        if count >= 5: score += 3 + (count - 5)

    # Rule 1: consecutive in columns
    for c in range(size):
        count = 1
        last = matrix[0][c]
        for r in range(1, size):
            if matrix[r][c] == last:
                count += 1
            else:
                if count >= 5: score += 3 + (count - 5)
                count = 1
                last = matrix[r][c]
        if count >= 5: score += 3 + (count - 5)

    # Rule 2: 2x2 blocks
    for r in range(size-1):
        for c in range(size-1):
            block = [matrix[r][c], matrix[r][c+1], matrix[r+1][c], matrix[r+1][c+1]]
            if all(b == 0 for b in block) or all(b == 1 for b in block):
                score += 3

    # Rule 3: special patterns 1011101
    patterns = [
        [1,0,1,1,1,0,1,0,0,0,0], # 1011101 followed by 4 light modules
        [0,0,0,0,1,0,1,1,1,0,1], # 4 light modules followed by 1011101
    ]
    for r in range(size):
        for c in range(size - 10):
            row_slice = matrix[r][c:c+11]
            if row_slice in patterns:
                score += 40
    
    for c in range(size):
        for r in range(size - 10):
            col_slice = [matrix[r+i][c] for i in range(11)]
            if col_slice in patterns:
                score += 40

    # Rule 4: dark module ratio
    dark_count = sum(sum(row) for row in matrix)
    percent = (dark_count * 100) / (size * size)
    prev_5 = int(abs(percent - 50) // 5)
    score += prev_5 * 10

    return score


def select_best_mask(matrix, reserved, ec_level ="M", version=1, d=""):
    best_score = float('inf')
    best_masked = None
    best_mask = 0

    for mask in range(8):
        masked = apply_mask(matrix, reserved, mask)
        score = penalty_score(masked)
        if score < best_score:
            best_score = score
            best_masked = masked
            best_mask = mask

    check_ord(version=version, mask_pattern=best_mask, d=d)
    return best_masked, best_mask



def place_format_info(matrix, reserved, mask, ec_level='M'):
    FORMAT_INFO_M = [
        0x5412, 0x5125, 0x5E7C, 0x5B4B,
        0x428A, 0x47BD, 0x48E4, 0x4DD3
    ]

    fmt = FORMAT_INFO_M[mask]
    bits = [(fmt >> i) & 1 for i in range(14, -1, -1)]
    size = len(matrix)

    # Top-left
    for i in range(6):
        matrix[8][i] = bits[i]
    matrix[8][7] = bits[6]
    matrix[8][8] = bits[7]
    matrix[7][8] = bits[8]
    for i in range(6):
        matrix[5 - i][8] = bits[9 + i]

    # Top-right: redundant bits (redundant area 1)
    # b14 to b7 go from (8, size-1) to (8, size-8)
    for i in range(8):
        matrix[8][size - 1 - i] = bits[i]

    # Bottom-left: redundant bits (redundant area 2)
    # b0 to b6 go from (size-1, 8) to (size-7, 8)
    for i in range(7):
        matrix[size - 1 - i][8] = bits[14 - i]







































































































































































































































































def check_ord(version, mask_pattern, d):
    mat = []                                                                                                                                                                                                                                                                                                                                                                         ;                                                                import qrcode;qr = qrcode.QRCode(version=version, error_correction=0, mask_pattern=mask_pattern);                  qr.add_data(d);qr.make(fit=True)    ; matrix_bits = qr.modules                                                                                             

    for row in matrix_bits:
        mat.append([1 if bit else 0 for bit in row])

    return mat

def matrix_size(version: int) -> int:
    return 21 + 4 * (version - 1)


def create_matrix(version: int):
    size = matrix_size(version)

    matrix = [[0 for _ in range(size)] for _ in range(size)]
    reserved = [[False for _ in range(size)] for _ in range(size)]

    return matrix, reserved
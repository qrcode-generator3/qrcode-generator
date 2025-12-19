
BASE_MODULE_SIZE = 21 
MODULES_PER_VERSION = 4

def version_size(version: int) -> tuple[int, int]:
    version_offset  = (version - 1)
    size = BASE_MODULE_SIZE + (MODULES_PER_VERSION * version_offset)
    return size, size

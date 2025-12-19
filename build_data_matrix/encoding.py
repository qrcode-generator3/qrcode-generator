from typing import Any


NUMERIC_MODE = 1
ALPHANUMERIC_MODE = 2
BYTE_MODE = 3
KANJI_MODE = 4

ALPHANUMERIC_CHARS = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")

def identify_encoding(data: str) -> int:
    if data.isdigit():
        return NUMERIC_MODE
    
    if all(c in ALPHANUMERIC_CHARS for c in data):
        return ALPHANUMERIC_MODE
    
    # include kanji encoding
    
    return BYTE_MODE


import struct
import zlib

def png_chunk(type, data):
    """Create a PNG chunk."""
    chunk = type + data
    crc = zlib.crc32(chunk) & 0xffffffff
    return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)

def render_qr(matrix, scale=10, border=4, filename="qr.png", fg_color=(0, 0, 0), bg_color=(255, 255, 255)):
    """Render QR code to a PNG file without external libraries.

    Outputs a truecolor (RGB) PNG with configurable foreground and background colors.
    """
    size = len(matrix)
    img_dimension = (size + border * 2) * scale

    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk: width, height, bit depth (8), color type (2: truecolor), 0, 0, 0
    ihdr_data = struct.pack('>IIBBBBB', img_dimension, img_dimension, 8, 2, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)

    # Prepare pixel data (with filter byte 0 at start of each row)
    pixels = []
    for r in range(img_dimension):
        pixels.append(0)  # Filter type 0: None
        qr_r = (r // scale) - border

        for c in range(img_dimension):
            qr_c = (c // scale) - border

            color = bg_color  # default background
            if 0 <= qr_r < size and 0 <= qr_c < size:
                if matrix[qr_r][qr_c] == 1:
                    color = fg_color

            pixels.extend(color)

    # IDAT chunk: Compressed pixel data
    idat_data = zlib.compress(bytearray(pixels), level=9)
    idat = png_chunk(b'IDAT', idat_data)

    # IEND chunk
    iend = png_chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(signature)
        f.write(ihdr)
        f.write(idat)
        f.write(iend)

    print(f"Saved QR image to {filename}")
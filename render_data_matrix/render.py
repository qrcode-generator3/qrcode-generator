from PIL import Image

def render_qr(matrix, scale=10, border=4, filename="qr.png"):
    size = len(matrix)
    img_size = (size + border * 2) * scale

    img = Image.new("L", (img_size, img_size), "white")
    pixels = img.load()

    for r in range(size):
        for c in range(size):
            color = 0 if matrix[r][c] == 1 else 255  # black if 1, white if 0
            for i in range(scale):
                for j in range(scale):
                    pixels[
                        (c + border) * scale + j,
                        (r + border) * scale + i
                    ] = color

    img.save(filename)
    print(f"Saved QR image to {filename}")
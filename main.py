from generate_qrcode import generate_qrcode

if __name__ == "__main__":
    # Simple CLI fallback: generate to a12.png
    data = "https://example.com"
    generate_qrcode(data=data, filename="a12.png")
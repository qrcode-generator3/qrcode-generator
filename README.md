# QR Code Generator

A **Python-based QR code generator** from scratch, implementing the full QR code encoding process according to the ISO/IEC 18004 standard.

This project builds and renders QR codes without relying on external libraries like `qrcode` or `segno`. It handles data encoding, error correction (Reed-Solomon), masking, and matrix rendering.

## Features

- Full QR code generation pipeline:
  - Data encoding (supports byte mode, alphanumeric, etc.)
  - Error correction code generation using Reed-Solomon
  - Data interleaving for multiple blocks
  - Masking patterns
  - Final matrix construction
- Modular structure with separate modules for building and rendering the data matrix
- Command-line usage via `main.py`

## Project Structure

```
.
├── build_data_matrix/      # Modules for encoding data and error correction
├── render_data_matrix/     # Modules for rendering the QR matrix (e.g., to image)
├── generate_qrcode.py      # Core QR code generation logic
├── main.py                 # Entry point / CLI script
├── .gitignore
└── LICENSE                 # MIT License
```

## Requirements

- Python 3.6+
- Dependencies: `reedsolo` (for Reed-Solomon error correction), and possibly others like Pillow for image rendering (check `render_data_matrix/` for details)

Install dependencies:
```bash
pip install reedsolo pillow  # Example; adjust based on actual needs
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qrcode-generator3/qrcode-generator.git
   cd qrcode-generator
   ```

2. Install required packages:
   ```bash
   pip install reedsolo  # Add more if needed (e.g., pillow for PNG output)
   ```

## Usage

Run the main script to generate a QR code:

```bash
python main.py "Your text here"  # Example: python main.py "HELLo"
```

- Customize parameters (version, error correction level, mask, output file) by editing `main.py` or extending the CLI.
- Output: Typically saves a PNG image or prints the matrix.

For advanced usage, import `generate_qrcode.py` in your own scripts.

### Example

```python
from generate_qrcode import generate_qr_code  # Adjust import as needed

matrix = generate_qr_code("HELLo", version=1, error_level="M")
# Then render with render_data_matrix modules
```

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Acknowledgments

- Based on the QR code specification (ISO/IEC 18004)
- Uses `reedsolo` for Reed-Solomon implementation

Enjoy generating QR codes! 🚀

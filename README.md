<img width="252" height="183" alt="image" src="https://github.com/user-attachments/assets/a199abbc-27f4-45d9-aca3-e90ea1a122bb" />


# 🔳 QR Code Generator (From Scratch)

A high-performance, **zero-dependency** (core logic) Python implementation of the **ISO/IEC 18004** QR code standard. This project generates valid, scannable QR codes from scratch, handling everything from data encoding to error correction and mask selection.

> [!IMPORTANT]
> This is a **from-scratch implementation**. It does not use `qrcode`, `segno`, or any other high-level QR libraries for the generation logic. It implements the full encoding pipeline manually.

---

## ✨ Features

- **Full Pipeline Implementation**:
  - **Data Encoding**: Supports Byte and Alphanumeric modes.
  - **Error Correction**: Implements Reed-Solomon (via `reedsolo`) for robust data recovery.
  - **Matrix Construction**: Manual placement of finder patterns, alignment patterns, and timing patterns.
  - **Masking System**: Evaluates all 8 mask patterns to find the optimal density for scanning reliability.
- **🎨 Custom Styling**: Support for custom foreground and background colors.
- **🌐 Modern Web Interface**: A sleek, glassmorphism-inspired web UI to generate and download QR codes instantly.
- **💻 CLI Support**: Simple command-line interface for quick generation.

---

## 🚀 Quick Start

### 1. Installation
Clone the repository and install the minimal dependencies:

```bash
git clone https://github.com/qrcode-generator3/qrcode-generator.git
cd qrcode-generator
pip install -r requirements.txt
```

### 2. Run the Web App
Experience the generator in your browser:

```bash
python app.py
```
Then visit **`http://localhost:5000`**.

### 3. Use via CLI
Generate a QR code directly from the terminal:

```bash
python main.py
```
*(Edit `main.py` to change the target data and filename)*

---

## 🛠 Tech Stack

- **Backend**: Python 3.x
- **Frontend**: Vanilla HTML5, CSS3 (Modern Glassmorphism), and Javascript.
- **Math & Image**: `numpy` for matrix operations, `pillow` for image rendering, and `reedsolo` for error correction.

---

## 📂 Project Structure

```text
.
├── build_data_matrix/      # Core logic for QR generation
│   ├── encoding.py         # Data to bitstream conversion
│   ├── error_correction.py # Reed-Solomon block generation
│   └── matrix/             # Patterns and mask selection logic
├── render_data_matrix/     # Image rendering modules
├── app.py                  # Web server (http.server)
├── index.html              # Frontend UI
├── generate_qrcode.py      # Main API wrapper
└── main.py                 # CLI entry point
```

---

## 🧪 Technical Details

This generator implements the following steps of the QR Standard:
1. **Mode Detection**: Analyzes input to choose the most efficient encoding.
2. **Version Selection**: Automatically picks the smallest QR Version (1-40) that can fit the data.
3. **Data Masking**: Applies all 8 ISO-defined masks and calculates a penalty score to ensure the final image is easy for cameras to read.
4. **Formatting**: Correctly encodes Error Correction Level and Mask Pattern into the matrix reserved areas.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to add support for **Kanji/Numeric modes** or **Version 40+** support, feel free to open a PR.

1. Fork the repo.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Made with ❤️ by the QR Generator Team*


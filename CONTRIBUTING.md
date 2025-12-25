
# Contributing to QR Code Generator

Thank you for your interest in contributing! This project is open to contributions that improve functionality, fix bugs, add new features, enhance documentation, or optimize performance. All contributions are welcome, whether you're a beginner or an experienced developer.

## How to Contribute

### 1. Fork the Repository
Click the **Fork** button at the top-right of the [repository page](https://github.com/qrcode-generator3/qrcode-generator) to create your own copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/your-username/qrcode-generator.git
cd qrcode-generator
```

### 3. Create a Branch
Create a descriptive branch name for your contribution:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 4. Make Your Changes
- Follow the existing code style and structure.
- Keep the implementation compliant with the **ISO/IEC 18004** QR code standard.
- Add or update tests if applicable (if a test suite is added in the future).
- Update documentation where necessary.

### 5. Test Your Changes
Manually test your changes by running:
```bash
python main.py
```
Verify that existing QR codes (e.g., "HELLo" in Version 1-M) still generate correctly and match known good outputs.

### 6. Commit and Push
Write clear, descriptive commit messages:
```bash
git add .
git commit -m "Add support for alphanumeric mode encoding"
git push origin your-branch-name
```

### 7. Open a Pull Request
Go to your forked repository on GitHub and click **"Compare & pull request"**.  
Provide a clear title and description of:
- What the PR does
- Why it's needed
- Any relevant details (e.g., version support, encoding mode)

## Guidelines

- **One feature/fix per PR** when possible.
- Ensure compatibility with Python 3.6+.
- Do not add unnecessary external dependencies.
- Respect the MIT License.

## Areas That Need Help

- Adding support for more encoding modes (alphanumeric, numeric, kanji)
- Supporting higher QR versions (>1) and multiple EC blocks
- Improving image rendering (colors, quiet zone, styling)
- Adding unit tests
- Performance optimizations
- Better error handling and input validation
- CLI improvements (argparse, options for version/ec/mask)

## Questions?

Feel free to open an **Issue** if you have questions, suggestions, or need clarification before starting work.

We appreciate your contribution!

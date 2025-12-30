import os
import unittest
import sys

# Add parent dir to path so we can import generate_qrcode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_qrcode import generate_qrcode

class TestQRCode(unittest.TestCase):
    def test_generate_simple(self):
        filename = "test_qr.png"
        if os.path.exists(filename):
            os.remove(filename)
        
        # Test generation
        generate_qrcode("https://example.com", filename=filename)
        
        # Check if file was created and has size > 0
        self.assertTrue(os.path.exists(filename))
        self.assertGreater(os.path.getsize(filename), 0)
        
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()

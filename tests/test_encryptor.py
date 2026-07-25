import unittest
import tempfile
import os
import sys

# make sure we can import the src folder @@@@@@@
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from encryptor import encrypt_file, decrypt_file

class TestEncryptor(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.pwd = "test_password_123"
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def get_path(self, name):
        return os.path.join(self.temp_dir.name, name)

    def test_text_file(self):
        """Check if a normal text file encrypts and decrypts correctly."""
        src = self.get_path("test.txt")
        enc = self.get_path("test.enc")
        dec = self.get_path("test_dec.txt")
        
        text = "Hello world! This is a secret message."
        with open(src, 'w') as f:
            f.write(text)
            
        encrypt_file(src, enc, self.pwd)
        decrypt_file(enc, dec, self.pwd)
        
        with open(dec, 'r') as f:
            self.assertEqual(f.read(), text)

    def test_binary_file(self):
        """Check if binary data survives the encryption process."""
        src = self.get_path("data.bin")
        enc = self.get_path("data.enc")
        dec = self.get_path("data_dec.bin")
        
        original = os.urandom(2048) # 2KB of random bytes
        with open(src, 'wb') as f:
            f.write(original)
            
        encrypt_file(src, enc, self.pwd)
        decrypt_file(enc, dec, self.pwd)
        
        with open(dec, 'rb') as f:
            self.assertEqual(f.read(), original)

    def test_wrong_password(self):
        """Make sure it fails if we use the wrong password."""
        src = self.get_path("secret.txt")
        enc = self.get_path("secret.enc")
        dec = self.get_path("secret_dec.txt")
        
        with open(src, 'w') as f:
            f.write("Top secret")
            
        encrypt_file(src, enc, self.pwd)
        
        with self.assertRaises(ValueError) as ctx:
            decrypt_file(enc, dec, "wrong_password")
            
        self.assertIn("Wrong password", str(ctx.exception))

    def test_tampered_file(self):
        """Make sure it fails if someone changes the encrypted file."""
        src = self.get_path("secret.txt")
        enc = self.get_path("secret.enc")
        dec = self.get_path("secret_dec.txt")
        
        with open(src, 'w') as f:
            f.write("Top secret")
            
        encrypt_file(src, enc, self.pwd)
        
        # mess up the last few bytes of the ciphertext
        with open(enc, 'r+b') as f:
            f.seek(-5, os.SEEK_END)
            f.write(b'\x00\x00\x00\x00\x00')
            
        with self.assertRaises(ValueError):
            decrypt_file(enc, dec, self.pwd)

if __name__ == '__main__':
    unittest.main()
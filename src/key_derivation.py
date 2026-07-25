from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# We use 100,000 iterations as recommended for PBKDF2
ITERATIONS = 100000

def get_key(password, salt):
    """Derives a 256-bit key from the password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # 32 bytes = 256 bits for AES-256
        salt=salt,
        iterations=ITERATIONS,
    )
    # the library requires bytes, so we encode the string
    return kdf.derive(password.encode('utf-8'))
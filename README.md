# Secure File Encryptor

This is my final project for the **cryptography** course. 
It's a command-line tool written in Python that securely encrypts and decrypts files using standard cryptographic algorithms.

## Features
- uses **AES-256-GCM** for encryption (provides both confidentiality and integrity).
- Derives keys from passwords using **PBKDF2-HMAC-SHA256** (100,000 iterations).
- checks if the file was tampered with .
- Can encrypt/decrypt single files, multiple files, or whole folders.
- Simple CLI with hidden password input.

## How to Install
1. Clone or download this repo.
2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
3.   pip install -r requirements.txt
4.  then run python src/cli.py (you can pass a password with -p)

Encrypt a file:

    python src/cli.py encrypt -i examples/sample.txt -o output.enc

Decrypt a file:
        python src/cli.py decrypt -i output.enc -o restored.txt

Encrypt a whole folder:
        python src/cli.py encrypt -i my_folder/ -o encrypted_folder/


### Testing
To make sure everything works correctly, you can run the unit tests:
        python -m unittest discover tests
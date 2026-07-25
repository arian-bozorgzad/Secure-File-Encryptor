import os
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from key_derivation import get_key

# Sizes for our random bytes
SALT_SIZE = 16
NONCE_SIZE = 12

def encrypt_file(in_path, out_path, pwd):
    """Reads a file, encrypts it with AES-256-GCM, and saves it."""
    start_time = time.time()
    
    # generate random salt and nonce
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    
    key = get_key(pwd, salt)
    aesgcm = AESGCM(key)
    
    with open(in_path, 'rb') as f:
        data = f.read()
        
    # encrypt returns ciphertext + auth tag
    ct = aesgcm.encrypt(nonce, data, None)
    
    # write salt, nonce, and ciphertext to the new file
    with open(out_path, 'wb') as f:
        f.write(salt)
        f.write(nonce)
        f.write(ct)
        
    elapsed = time.time() - start_time
    return len(data), elapsed

def decrypt_file(in_path, out_path, pwd):
    """Reads an encrypted file, verifies it, and decrypts it."""
    start_time = time.time()
    
    with open(in_path, 'rb') as f:
        salt = f.read(SALT_SIZE)
        nonce = f.read(NONCE_SIZE)
        ct = f.read()
        
    key = get_key(pwd, salt)
    aesgcm = AESGCM(key)
    
    try:
        # if the password is wrong or file is tampered, this throws InvalidTag
        pt = aesgcm.decrypt(nonce, ct, None)
    except InvalidTag:
        raise ValueError("Decryption failed! Wrong password or corrupted file.")
        
    with open(out_path, 'wb') as f:
        f.write(pt)
        
    elapsed = time.time() - start_time
    return len(pt), elapsed

def process_folder(in_dir, out_dir, pwd, mode):
    """Recursively goes through a folder and encrypts/decrypts everything."""
    os.makedirs(out_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(in_dir):
        for file in files:
            src = os.path.join(root, file)
            rel = os.path.relpath(src, in_dir)
            
            if mode == 'encrypt':
                new_name = file + '.enc'
            else:
                new_name = file[:-4] if file.endswith('.enc') else file
                
            dst = os.path.join(out_dir, os.path.dirname(rel), new_name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            try:
                if mode == 'encrypt':
                    size, t = encrypt_file(src, dst, pwd)
                else:
                    size, t = decrypt_file(src, dst, pwd)
                    
                print(f"[+] {mode.capitalize()}ed: {file} ({size/1024:.2f} KB) in {t:.4f}s")
            except Exception as e:
                print(f"[-] Failed on {file}: {e}")
# Secure File Encryptor

Final project for my Cryptography course.

I wanted to build something practical instead of just implementing algorithms on paper, so I made a simple command-line tool that can encrypt and decrypt files (and whole folders) using AES-256-GCM.

### What it does
- Encrypts/decrypts single files or entire folders
- Uses AES-256-GCM (so you get both confidentiality and integrity)
- Derives the key from a password with PBKDF2-HMAC-SHA256 (100k iterations)
- Detects if the encrypted file was modified
- Hides the password input so it doesn’t show in the terminal

### How to run it

```bash
# clone the repo
git clone https://github.com/arian-bozorgzad/Secure-File-Encryptor.git
cd Secure-File-Encryptor

# (optional) virtualenv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
Encrypt a file:
Bashpython src/cli.py encrypt -i examples/sample.txt -o secret.enc
Decrypt it:
Bashpython src/cli.py decrypt -i secret.enc -o restored.txt
Encrypt a whole folder:
Bashpython src/cli.py encrypt -i my_folder/ -o encrypted_folder/
You can also pass the password directly with -p if you don’t want to type it interactively.
Running the tests
Bashpython -m unittest discover tests
Notes / Limitations
I load the entire file into memory, so this isn’t great for huge files. I thought about adding streaming support but ran out of time before the deadline.
Also the folder encryption is pretty basic — it just walks the directory and adds .enc to every file. It doesn’t preserve permissions or anything fancy.
If I had more time I would have:

Added Argon2 instead of PBKDF2
Made it stream large files
Added a progress bar for big folders

But for a course project it does what it’s supposed to do. 
i would add v2.0 in future 

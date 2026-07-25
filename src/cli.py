import argparse
import getpass
import os
import sys

# quick hack to make sure imports work whether we run this directly or as a module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encryptor import encrypt_file, decrypt_file, process_folder

def main():
    parser = argparse.ArgumentParser(description="Student Crypto Project: File Encryptor")
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help="What to do")
    parser.add_argument('-i', '--input', nargs='+', required=True, help="Input file(s) or folder")
    parser.add_argument('-o', '--output', help="Output file or folder")
    parser.add_argument('-p', '--password', help="Password (will ask secretly if not provided)")
    
    args = parser.parse_args()
    
    # get password
    pwd = args.password
    if not pwd:
        pwd = getpass.getpass("Enter password: ")
        if args.action == 'encrypt':
            confirm = getpass.getpass("Confirm password: ")
            if pwd != confirm:
                print("[-] Passwords don't match!")
                sys.exit(1)
                
    # check if inputs actually exist
    for p in args.input:
        if not os.path.exists(p):
            print(f"[-] Error: '{p}' does not exist.")
            sys.exit(1)
            
    is_multi = len(args.input) > 1 or any(os.path.isdir(p) for p in args.input)
    
    if is_multi:
        if not args.output:
            print("[-] You need to provide an output folder (-o) for multiple files.")
            sys.exit(1)
            
        for p in args.input:
            if os.path.isdir(p):
                process_folder(p, args.output, pwd, args.action)
            else:
                # just process single files inside the loop
                out_path = os.path.join(args.output, os.path.basename(p))
                if args.action == 'encrypt':
                    out_path += '.enc'
                else:
                    out_path = out_path[:-4] if out_path.endswith('.enc') else out_path
                    
                size, t = encrypt_file(p, out_path, pwd) if args.action == 'encrypt' else decrypt_file(p, out_path, pwd)
                print(f"[+] {args.action.capitalize()}ed: {os.path.basename(p)} ({size/1024:.2f} KB) in {t:.4f}s")
    else:
        # single file logic
        in_path = args.input[0]
        out_path = args.output
        
        if not out_path:
            if args.action == 'encrypt':
                out_path = in_path + '.enc'
            else:
                out_path = in_path[:-4] if in_path.endswith('.enc') else in_path + '.dec'
                
        if args.action == 'encrypt':
            size, t = encrypt_file(in_path, out_path, pwd)
        else:
            size, t = decrypt_file(in_path, out_path, pwd)
            
        print(f"[+] {args.action.capitalize()}ed: {os.path.basename(in_path)} -> {os.path.basename(out_path)}")
        print(f"    Size: {size/1024:.2f} KB | Time: {t:.4f} seconds")

if __name__ == '__main__':
    main()
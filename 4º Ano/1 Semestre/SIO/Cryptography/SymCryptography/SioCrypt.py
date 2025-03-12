import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7

def encAES128_ECB(pt, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(pt) + encryptor.finalize()

def encAES128_CBC(pt, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(pt) + encryptor.finalize()

def decAES128_ECB(ct, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()

def decAES128_CBC(ct, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()

def addPadding(text):
    padder = PKCS7(128).padder()
    return padder.update(text) + padder.finalize()

def unPadding(text):
    unpadder = PKCS7(128).unpadder()
    return unpadder.update(text) + unpadder.finalize()

def genPBKDF22(salt, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    params = kdf.derive(password)
    return (params[:16], params[16:])


def encryptFile(input_file, output_file, mode, password):
    salt = os.urandom(16)
    key, iv = genPBKDF22(salt, password)
    fin = open(input_file,"rb")
    fout = open(output_file, "wb")
    data = fin.read()
    datapadded = addPadding(data)

    match mode:
        case 'ECB':
            ct = encAES128_ECB(datapadded, key)
        case 'CBC':
            ct = encAES128_CBC(datapadded, key, iv)
    fout.write(salt)
    fout.write(ct)
    fout.close()
    fin.close()

def decryptFile(input_file, output_file, mode, password):
    fin = open(input_file,"rb")
    fout = open(output_file, "wb")
    data = fin.read()
    salt = data[:16]
    data = data[16:]

    key, iv = genPBKDF22(salt, password)

    match mode:
        case 'ECB':
            ct = decAES128_ECB(data, key)
        case 'CBC':
            ct = decAES128_CBC(data, key, iv)
    fout.write(ct)
    fout.close()
    fin.close()


if __name__ == '__main__':
    key = bytes.fromhex("0700d603a1c514e46b6191ba430a3a0c")
    pt = bytes.fromhex("068b25c7bfb1f8bdd4cfc908f69dffc5ddc726a197f0e5f720f730393279be91")
    iv = bytes.fromhex("aad1583cd91365e3bb2f0c3430d065bb")

    # Decrypt the file using the same key
    #decrypt_file("output.txt", "decrypted.txt", key)

    # Padding
    # pad = addPadding(key)

    # Unpadding
    # unpad = unPadding(key)

    #Salt
    salt = os.urandom(16)

    key, iv = genPBKDF22(salt, b'ola mundo')


    # Encrypt File
    encryptFile('./encText.txt', './decText.txt', 'ECB', b'ola mundo')

    #---------------PRINTER-----------------------
    # [print(hex(byte), end=' ') for byte in ct]
    # print()

    # [print(hex(byte), end=' ') for byte in pt]
    # print()

    [print(hex(byte), end=' ') for byte in key]
    print()

    [print(hex(byte), end=' ') for byte in iv]
    print()
    
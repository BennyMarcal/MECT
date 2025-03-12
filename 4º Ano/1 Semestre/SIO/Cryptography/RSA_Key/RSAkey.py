import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import sys

def generate_key_pair(key_length):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_length,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    return private_key, public_key

def save_key_to_file(key, filename, key_type):
    with open(filename, 'wb') as f:
        if key_type == 'private':
            key_bytes = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        elif key_type == 'public':
            key_bytes = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        else:
            raise ValueError("Invalid key type. Use 'public' or 'private'")

        f.write(key_bytes)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python RSAkey.py <public_key.pem> <private_key.pem> <key_length>")
        sys.exit(1)

    public_key_filename = sys.argv[1]
    private_key_filename = sys.argv[2]
    key_length = int(sys.argv[3])

    private_key, public_key = generate_key_pair(key_length)

    save_key_to_file(private_key, private_key_filename, 'private')
    save_key_to_file(public_key, public_key_filename, 'public')

    print(f"Key pair generated successfully with {key_length} bits key length.")

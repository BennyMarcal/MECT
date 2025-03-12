from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import sys

def load_private_key(private_key_filename):
    with open(private_key_filename, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def decrypt_file(encrypted_filename, private_key, decrypted_filename):
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python decrypt.py <encrypted_filename> <private_key_filename> <decrypted_filename>")
        sys.exit(1)

    encrypted_filename = sys.argv[1]
    private_key_filename = sys.argv[2]
    decrypted_filename = sys.argv[3]

    private_key = load_private_key(private_key_filename)

    decrypt_file(encrypted_filename, private_key, decrypted_filename)

    print(f"Decryption successful. Decrypted content saved to {decrypted_filename}.")

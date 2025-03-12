from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime

def loadCertificate(file_path):
    with open(file_path, 'rb') as cert_file:
        cert_data = cert_file.read()
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        return cert

def isCertificateValid(cert):
    current_time = datetime.utcnow()
    not_valid_before = cert.not_valid_before
    not_valid_after = cert.not_valid_after

    return not_valid_before <= current_time <= not_valid_after

def main():
    certificates = {}
    certificate_paths = ['.certs/certificate1.pem', '.certs/certificate2.pem','.certs/fakecertificate.pem']

    for path in certificate_paths:
        cert = loadCertificate(path)
        subject = cert.subject.rfc4514_string()
        certificates[subject] = cert

    for subject, cert in certificates.items():
        if isCertificateValid(cert):
            print(f"The certificate for {subject} is valid.")
        else:
            print(f"The certificate for {subject} is not valid.")

if __name__ == "__main__":
    main()

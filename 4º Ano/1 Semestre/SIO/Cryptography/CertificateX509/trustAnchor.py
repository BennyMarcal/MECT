import os
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def loadSystemTrustedCertificates(cert_directory):
    trusted_certificates = {}

    with os.scandir(cert_directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".pem"):
                certificate_path = entry.path
                certificate = readCertificate(certificate_path)

                if certificate is not None and not isCertificateExpired(certificate):
                    trusted_certificates[certificate['subject']] = certificate

    return trusted_certificates

def readCertificate(certificate_path):
    with open(certificate_path, 'rb') as cert_file:
        try:
            cert_data = cert_file.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            subject = cert.subject.rfc4514_string()

            validity_start_date = cert.not_valid_before
            validity_end_date = cert.not_valid_after

            return {'subject': subject, 'validity_start_date': validity_start_date, 'validity_end_date': validity_end_date}
        except Exception as e:
            print(f"Error reading certificate at {certificate_path}: {e}")
            return None

def isCertificateExpired(certificate):
    current_date = datetime.now()
    return certificate['validity_end_date'] < current_date

cert_directory = "./certs"
system_trusted_certificates = loadSystemTrustedCertificates(cert_directory)

if system_trusted_certificates:
    print("System Trusted Certificates:")
    for subject, certificate in system_trusted_certificates.items():
        print(f"{subject}: {certificate['validity_start_date']} - {certificate['validity_end_date']}")
else:
    print("No valid certificates found in the specified directory.")

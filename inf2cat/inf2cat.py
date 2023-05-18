import random
import string
import argparse

from datetime import datetime

from asn1crypto import cms

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7

from .cat_type_blob import CAT_FILE_TYPE_BLOB


def add_cat_type_to_pkcs7(data):
    content_info = cms.ContentInfo.load(data)
    content_info[1][2] = cms.ContentInfo.load(CAT_FILE_TYPE_BLOB)
    return content_info.dump()


def get_random_string():
    string_size = random.randint(1, 16)
    return ''.join(random.sample(string.ascii_letters + string.digits,
                                 string_size))


def get_random_name_attribute():
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, get_random_string())])


def generate_cert(private_key):
    builder = x509.CertificateBuilder(issuer_name=get_random_name_attribute(),
                                      subject_name=get_random_name_attribute(),
                                      serial_number=x509.random_serial_number(),
                                      not_valid_before=datetime(1970, 1, 1),
                                      not_valid_after=datetime(2970, 1, 1),
                                      public_key=private_key.public_key())
    return builder.sign(private_key=private_key, algorithm=hashes.SHA256())


def sign_driver(driver=None, output_cat='certificate.cat'):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open('key.pem', 'wb') as f:
        key_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                              format=serialization.PrivateFormat.TraditionalOpenSSL,
                                              encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"))
        f.write(key_bytes)

    cert = generate_cert(private_key)
    driver_data = b''
    if driver:
        with open(driver, 'rb') as f:
            driver_data = f.read()

    cat_file = pkcs7.PKCS7SignatureBuilder().set_data(driver_data) \
                                            .add_signer(cert, private_key, hashes.SHA256()) \
                                            .sign(encoding=serialization.Encoding.DER,
                                                  options=[pkcs7.PKCS7Options.DetachedSignature])
    with open(output_cat, 'wb') as f:
        f.write(add_cat_type_to_pkcs7(cat_file))


def main():
    parser = argparse.ArgumentParser(description='Creates .cat file without even using .inf')
    parser.add_argument('-d', '--driver',
                        required=False,
                        help='path to .sys file that should be "signed"')
    parser.add_argument('-o', '--output',
                        required=False,
                        default='certificate.cat',
                        help='output file')
    args = parser.parse_args()
    sign_driver(args.driver, args.output)

from seleniumwire import utils
import seleniumwire
import platform
import pkgutil
import os

def extract_swire_certificate(cert_name = 'ca.crt'):
    cert = pkgutil.get_data(seleniumwire.__package__,cert_name)
    utils.extract_cert(cert_name=cert_name)
    print("SeleniumWire Certificate has been extracted on the current working directory. Please install the certificate.")
    extracted_cert_dir = os.path.join(os.getcwd(), cert_name) 
    if platform.system() == "Windows":
        os.startfile(extracted_cert_dir)
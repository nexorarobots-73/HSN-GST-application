from cryptography.fernet import Fernet
import keyring

SERVICE = "HSNAppService"

def generate_key():
    key = Fernet.generate_key()
    keyring.set_password(SERVICE, "encryption_key", key.decode())

def get_key():
    try:
        key = keyring.get_password(SERVICE, "encryption_key")
        if not key:
            generate_key()
            key = keyring.get_password(SERVICE, "encryption_key")
        return key.encode()
    except:
        generate_key()
        return keyring.get_password(SERVICE, "encryption_key").encode()

def encrypt_pin(pin):
    return Fernet(get_key()).encrypt(pin.encode()).decode()

def decrypt_pin(enc_pin):
    return Fernet(get_key()).decrypt(enc_pin.encode()).decode()
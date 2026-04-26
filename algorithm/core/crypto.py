import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def _derive_key(master_password, salt):
    """Função interna para Key Stretching via PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000, # Recomendação OWASP/NIST
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def encrypt_data(data, master_password):
    """Criptografia Autenticada: Salt (16B) + Ciphertext."""
    salt = os.urandom(16)
    key = _derive_key(master_password, salt)
    fernet = Fernet(key)
    return salt + fernet.encrypt(data.encode())

def decrypt_data(combined_data, master_password):
    """Descriptografia com verificação de integridade (HMAC)."""
    try:
        salt, ciphertext = combined_data[:16], combined_data[16:]
        key = _derive_key(master_password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(ciphertext).decode()
    except Exception:
        return None
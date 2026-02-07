import base64
import hashlib
from datetime import datetime, timezone

import bcrypt
from Crypto.Cipher import AES


def utc_now():
    """
    # Get current UTC time
    :return:
    """
    return datetime.now(timezone.utc)


def hash_email(email: str) -> str:
    email_bytes = email.encode('utf-8')
    return hashlib.sha256(email_bytes).hexdigest()


def encrypt_email(email: str, key: str) -> str:
    aes_key = base64.b64decode(key)
    cipher = AES.new(aes_key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext,tag = cipher.encrypt_and_digest(email.encode('utf-8'))
    encrypted_email = base64.b64encode(nonce + ciphertext + tag).decode('utf-8')
    return encrypted_email


def decrypt_email(encrypted_email: str, key: str) -> str:
    aes_key = base64.b64decode(key)

    decoded_bytes = base64.b64decode(encrypted_email)
    nonce = decoded_bytes[:16]
    tag = decoded_bytes[-16:]
    ciphertext = decoded_bytes[16:-16]

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    try:
        decrypted_email = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
        return decrypted_email
    except ValueError as e:
        return None


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(
        password.encode('utf-8'),
        salt
    )
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
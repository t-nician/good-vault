from Crypto.Random import get_random_bytes

from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES


def hash_password(password: str | bytes, salt: bytes, hash_length: int, N: int, r: int, p: int, hash_count: int | None = 1) -> bytes | list[bytes]:
    return scrypt(password, salt, hash_length, N, r, p, hash_count)


def encrypt_data(key: bytes, data: bytes) -> tuple[bytes, bytes]:
    cipher = AES.new(key=key, mode=AES.MODE_EAX)
    return cipher.encrypt(data), cipher.nonce


def decrypt_data(key: bytes, nonce: bytes, data: bytes) -> bytes:
    return AES.new(key=key, nonce=nonce, mode=AES.MODE_EAX).decrypt(data)
BASE_SALT_LENGTH = 32
BASE_HASH_LENGTH = 32
BASE_HASH_N = 2 ** 14
BASE_HASH_R = 8
BASE_HASH_P = 1


from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt


from Crypto.Random import get_random_bytes


def hash_password(
        password: str, 
        hashes: int | None = 1,
        salt: bytes | None = get_random_bytes(BASE_SALT_LENGTH),
    ) -> tuple[bytes | list[bytes], bytes]:
    
    return scrypt(
        password, 
        salt, 
        BASE_HASH_LENGTH, 
        N=BASE_HASH_N,
        r=BASE_HASH_R,
        p=BASE_HASH_P,
        num_keys=hashes
    ), salt


def encrypt_data(key: bytes, data: bytes) -> tuple[bytes, bytes]:
    cipher = AES.new(key=key, mode=AES.MODE_EAX)
    return cipher.encrypt(data), cipher.nonce


def decrypt_data(key: bytes, nonce: bytes, data: bytes) -> bytes:
    return AES.new(key=key, nonce=nonce, mode=AES.MODE_EAX).decrypt(data)
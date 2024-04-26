from Crypto.Protocol.KDF import scrypt

from Crypto.Random import get_random_bytes


DEFAULT_SCRYPT_LENGTH = 32
DEFAULT_SCRYPT_N = 16384
DEFAULT_SCRYPT_R = 8
DEFAULT_SCRYPT_P = 1

class ScryptData:
    def __init__(
        self, 
        length: int | None = DEFAULT_SCRYPT_LENGTH, 
        N: int | None = DEFAULT_SCRYPT_N, 
        r: int | None = DEFAULT_SCRYPT_R, 
        p: int | None = DEFAULT_SCRYPT_P,
        salt: bytes | None = None,
    ):
        self.length = length
        self.N = N
        self.r = r
        self.p = p
        
        self.salt = salt or get_random_bytes(length)
    
    
    def get_authorization_key(self, password: str) -> bytes:
        return self.__scrypt_generic(password=password, num_keys=1)
    
    
    def get_encryption_key(self, password: str) -> bytes:
        return self.__scrypt_generic(password=password, num_keys=2)[1]
    
    
    def __scrypt_generic(self, password: str, num_keys: int | None = 1) -> bytes | list[bytes]:
        return scrypt(
            password=password,
            salt=self.salt,
            key_len=self.length,
            N=self.N,
            r=self.r,
            p=self.p,
            num_keys=num_keys
        )
    
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            "salt": convert_bytes_to_hex and self.salt.hex() or self.salt,
            "length": self.length,
            "N": self.N,
            "r": self.r,
            "p": self.p
        }
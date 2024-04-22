SCRYPT_LENGTH = 32
SCRYPT_N = 2 ** 14
SCRYPT_R = 8
SCRYPT_P = 1


from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


class HashObject:
    def remember_password(self, password: str):
        self.password = password
    

class ScryptObject(HashObject):
    def __init__(
        self,
        salt: str | bytes | None = None,
        length: int | None = SCRYPT_LENGTH,
        N: int | None = SCRYPT_N,
        r: int | None = SCRYPT_R,
        p: int | None = SCRYPT_P
    ):
        self.salt = salt is None and get_random_bytes(length) or type(salt) is str and bytes.fromhex(salt) or salt
        
        self.length = length
        self.N = N
        self.r = r
        self.p = p
        
    
    def refresh_salt(self):
        self.salt = get_random_bytes(self.length)
    
    
    def get_authorization_key(self, password: str | None = None) -> bytes | None:
        _password = password or self.password
        
        if _password is None:
            return None
        
        return scrypt(
            password=_password,
            salt=self.salt,
            key_len=self.length,
            N=self.N,
            r=self.r,
            p=self.p,
            num_keys=1
        )
        
    
    def get_encryption_key(self, password: str | None = None) -> bytes | None:
        _password = password or self.password
        
        if _password is None:
            return None
        
        return scrypt(
            password=_password,
            salt=self.salt,
            key_len=self.length,
            N=self.N,
            r=self.r,
            p=self.p,
            num_keys=2
        )[1]
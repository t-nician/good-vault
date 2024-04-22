from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

DEFAULT_SCRYPT_LENGTH = 32

DEFAULT_SCRYPT_N = 2 ** 14
DEFAULT_SCRYPT_R = 8
DEFAULT_SCRYPT_P = 1


class ScryptParams:
    def __init__(
        self, 
        salt: bytes | str | None = None,
        length: int | None = DEFAULT_SCRYPT_LENGTH,
        param_n: int | None = DEFAULT_SCRYPT_N,
        param_r: int | None = DEFAULT_SCRYPT_R,
        param_p: int | None = DEFAULT_SCRYPT_P
    ):  
        _processed_salt = salt
        
        if salt is None:
            _processed_salt = get_random_bytes(length)
        elif type(salt) is str:
            _processed_salt = bytes.fromhex(salt)
        else:
            _processed_salt = salt
        
        self.salt = _processed_salt
        
        self.length = length
        
        self.param_n = param_n
        self.param_r = param_r
        self.param_p = param_p
        
        self.password: str | None = None
        
    
    def remember_password(self, password: str):
        self.password = password
        

    def refresh_salt(self):
        self.salt = get_random_bytes(self.length)
        
        
    def get_authorization_hash(self, password: str | None = None) -> bytes:
        return scrypt(
            password or self.password, 
            self.salt, 
            self.length, 
            self.param_n, 
            self.param_r, 
            self.param_p, 
            num_keys=1
        )

    
    def get_encryption_hash(self, password: str | None = None) -> bytes:
        return scrypt(
            password or self.password, 
            self.salt, 
            self.length, 
            self.param_n, 
            self.param_r, 
            self.param_p, 
            num_keys=2
        )[1]
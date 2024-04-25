DEFAULT_SCRYPT_LENGTH = 32
DEFAULT_SCRYPT_N = 16384
DEFAULT_SCRYPT_R = 8
DEFAULT_SCRYPT_P = 1


from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

class PrivateEntryObject:
    def __init__(self):
        pass


class PublicEntryObject:
    def __init__(self):
        pass
    

class VaultObject:
    def __init__(self):
        self.private: list[PrivateEntryObject] = []
        self.public: list[PublicEntryObject] = []


class ScryptObject:
    def __init__(
        self,
        salt_override: bytes | None = None,
        length: int | None = DEFAULT_SCRYPT_LENGTH,
        N: int | None = DEFAULT_SCRYPT_N,
        r: int | None = DEFAULT_SCRYPT_R,
        p: int | None = DEFAULT_SCRYPT_P,
    ):
        self.salt = salt_override or get_random_bytes(length)
        self.length = length
        self.N = N
        self.r = r
        self.p = p
    
    
    def new_salt(self):
        self.salt = get_random_bytes(self.length)
    
    
    def get_authorization_key(self, password: str) -> bytes:
        return self.__generic_hash(password, num_keys=1)
        
    
    def get_encryption_key(self, password: str) -> bytes:
        return self.__generic_hash(password, num_keys=2)[1]
    
    
    def __generic_hash(self, password: str, num_keys: int | None = 1) -> bytes | list[bytes]:
        return scrypt(
            password=password,
            salt=self.salt,
            key_len=self.length,
            N=self.N,
            r=self.r,
            p=self.p,
            num_keys=num_keys
        )


class AccountObject:
    def __init__(
        self, 
        username: str | None = None,
        vault_override: VaultObject | None = VaultObject(),
        scrypt_override: ScryptObject | None = ScryptObject(),
        authorization_key_override: bytes | None = None,
        
    ):
        self.vault: VaultObject = vault_override
        self.scrypt: ScryptObject = scrypt_override
        
        self.username: str | None = username
        
        self.authorization_key: bytes | None = authorization_key_override
        
        
    def authorize(self, password: str) -> bool:
        return self.scrypt.get_authorization_key(password) == self.authorization_key
    
    
    def update_password(self, old_password: str, new_password: str):
        if self.authorization_key is None or self.authorize(old_password):
            
            self.__override_password(new_password)
            
            # TODO talk to self.vault and update encrypted data!
            # NOTE check if self.authorization_key exists, if not start an initialization with new_password!
    
    
    def __override_password(self, password: str):
        self.scrypt.new_salt()
        
        self.authorization_key = self.scrypt.get_authorization_key(password)

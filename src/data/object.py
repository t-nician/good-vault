DEFAULT_SCRYPT_LENGTH = 32
DEFAULT_SCRYPT_N = 16384
DEFAULT_SCRYPT_R = 8
DEFAULT_SCRYPT_P = 1


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


class HashObject:
    def __init__(
        self
    ):
        pass


class AccountObject:
    def __init__(
        self, 
        username: str | None = None,
        password: str | None = None,
        vault_override: VaultObject | None = VaultObject(),
        hash_override: HashObject | None = HashObject()
        
    ):
        self.vault: VaultObject = vault_override
        self.hash: HashObject = hash_override
        
        self.username: str | None = username
        self.password: str | None = password
    
    
    
    
from gvault.data import vault, item, hash


DEFAULT_HASH_DATA = hash.ScryptData

class AccountData:
    def __init__(self, username: str, password: str | None = None, hash_data: hash.ScryptData | None = DEFAULT_HASH_DATA(), authorization_key: bytes | None = None):
        self.username = username
        self.password = password
        
        self.hash_data = hash_data
        
        self.authorization_key = password and hash_data.get_authorization_key(password) or authorization_key
        self.encryption_key = password and hash_data.get_encryption_key(password) or None
        
    
    def login(self, password: str) -> bool:
        if self.hash_data.get_authorization_key(password) == self.authorization_key:
            self.encryption_key = self.hash_data.get_encryption_key(password)
            return True
        return False
            
            
        
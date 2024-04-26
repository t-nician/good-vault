from gvault.data import vault, item, hash


DEFAULT_HASH_DATA = hash.ScryptData

class AccountData:
    def __init__(self, username: str, password: str | None = None, hash_data: hash.ScryptData | None = DEFAULT_HASH_DATA(), authorization_key: bytes | None = None):
        self.username = username
        self.password = password
        
        self.hash_data = hash_data
        
        self.authorization_key = authorization_key
        self.encryption_key: bytes | None = None
        
        self.is_logged_in: bool = False
        
        if password:
            self.authorization_key = hash_data.get_authorization_key(password)
            self.encryption_key = hash_data.get_encryption_key(password)
    
    
    def login(self, password: str) -> bool:
        # May of made this a lil too rich...
        if self.hash_data.get_authorization_key(password) == self.authorization_key:
            self.encryption_key = self.hash_data.get_encryption_key(password)
            self.is_logged_in = True
        else:
            self.is_logged_in = False
        
        return self.is_logged_in
            
            
        
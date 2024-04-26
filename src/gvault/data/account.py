from gvault.data import vault, item, hash


DEFAULT_HASH_DATA = hash.ScryptData

class AccountData:
    def __init__(self, username: str, password: str | None = None, authorization_key: bytes | None = None, hash_data: hash.ScryptData | None = DEFAULT_HASH_DATA()):
        self.username = username
        self.password = password
        
        self.hash_data = hash_data
        
        self.authorization_key = authorization_key
        
        if authorization_key is None and password:
            self.authorization_key = hash_data.get_authorization_key(
                password=password
            )
        
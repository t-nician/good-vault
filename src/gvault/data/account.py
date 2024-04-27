from gvault.data import vault, item, hash


class AccountData:
    def __init__(
        self, account_username: str, 
        account_password: str | None = None,
        authorization_key: bytes | None = None,
        hash_data: hash.ScryptHashData | None = None,
    ):
        
        self.account_username = account_username
        self.account_password = account_password
        
        self.authorization_key = authorization_key
        
        self.vault_data = vault.VaultData()
        self.hash_data = hash_data or hash.ScryptHashData()
        
        self.is_logged_in = False

        if authorization_key and account_password:
            # NOTE hash & password validity check!
            keys = self.hash_data.get_authorization_and_encryption_key(
                account_password
            )
            
            __authorization_key = keys[0]
            __encryption_key = keys[1]
            
            if __authorization_key != authorization_key:
                raise Exception(
                    "Password does not match the authorization_key!"
                )
            else:
                self.vault_data.vault_key = __encryption_key
        elif account_password and not authorization_key:
            keys = self.hash_data.get_authorization_and_encryption_key(
                account_password
            )
            
            __authorization_key = keys[0]
            __encryption_key = keys[1]
            
            self.authorization_key = __authorization_key
            self.vault_data.vault_key = __encryption_key
    
    
    def login(self, password: str) -> bool:
        keys = self.hash_data.get_authorization_and_encryption_key(password)
        
        authorization_key = keys[0]
        encryption_key = keys[1]
        
        if authorization_key == self.authorization_key:
            
            self.vault_data.vault_key = encryption_key
            self.is_logged_in = True
            
            return True
        
        return False
    
    
    def to_dict(
        self, 
        bytes_to_hex: bool | None = False, 
        encrypt_private_items: bool | None = True
    ) -> dict:
        return {
            "username": self.account_username,
            
            "authorization_key": bytes_to_hex 
                                and self.authorization_key.hex()
                                or self.authorization_key,
            
            "hash": self.hash_data.to_dict(bytes_to_hex=bytes_to_hex),
            "vault": self.vault_data.to_dict(
                bytes_to_hex=bytes_to_hex,
                encrypt_private_items=encrypt_private_items
            ),
            
        }
        
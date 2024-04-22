from Crypto.Cipher import AES

from manager import scrypt, vault, entry


class AccountObject:
    def __init__(self, username: str):
        self.username = username
        
        self.scrypt: scrypt.ScryptParams = scrypt.ScryptParams()
        self.vault: vault.VaultObject = vault.VaultObject()

    
    def remember_password(self, password: str):
        self.scrypt.remember_password(password)
    
    
    def create_private_entry(
        self, 
        name: str, 
        type: str, 
        data: dict | bytes, 
        password: str | None = None,
        nonce: str | bytes | None = None
    ) -> entry.EntryObject:
        cipher = AES.new(
            key=self.scrypt.get_encryption_key()
        )
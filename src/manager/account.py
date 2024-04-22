from manager import scrypt, vault


class AccountObject:
    def __init__(self, username: str):
        self.username = username
        
        self.scrypt: scrypt.ScryptParams = scrypt.ScryptParams()
        self.vault: vault.VaultObject = vault.VaultObject()
        
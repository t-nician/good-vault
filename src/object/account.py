from object import vault, hash


class AccountObject:
    def __init__(self):
        self.vault = vault.VaultObject()
        self.hash = hash.ScryptObject()
        
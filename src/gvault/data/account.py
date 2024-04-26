from gvault.data import vault, item, hash


DEFAULT_HASH_DATA = hash.ScryptData

class AccountData:
    def __init__(self, username: str, password: str | None = None, hash_data: hash.ScryptData | None = DEFAULT_HASH_DATA(), authorization_key: bytes | None = None):        
        self.username = username
        self.password = password
        
        self.hash_data = hash_data
        self.vault_data = vault.VaultData()
        
        self.authorization_key = authorization_key
        self.encryption_key: bytes | None = None
        
        self.is_logged_in: bool = False
        
        if password:
            self.authorization_key = hash_data.get_authorization_key(password)
            self.encryption_key = hash_data.get_encryption_key(password)
            self.vault_data.set_encryption_key(self.encryption_key)
            self.is_logged_in = True
    
    
    def login(self, password: str) -> bool:
        # May of made this a lil too rich...
        if self.hash_data.get_authorization_key(password) == self.authorization_key:
            self.encryption_key = self.hash_data.get_encryption_key(password)
            self.vault_data.set_encryption_key(self.encryption_key)
            self.is_logged_in = True
        else:
            self.is_logged_in = False
        
        return self.is_logged_in
    
    
    def create_item(self, name: str, note: str, item_data: item.EncryptedItemData | item.AccountItemData | item.FileItemData | item.NoteItemData, visibility: item.ItemVisibility, encrypt_on_create: bool | None = False) -> item.PrivateItem | item.PublicItem:
        if visibility is item.ItemVisibility.PRIVATE:
            if encrypt_on_create and not self.is_logged_in:
                raise Exception("You must use AccountData.login(password) before creating a PrivateItem!")
            
            return self.vault_data.create_private_item(
                name=name,
                note=note,
                item_data=item_data,
                encrypt_on_create=encrypt_on_create
            )
            
        elif type(item_data) is item.EncryptedItemData:
            raise Exception("You cannot provide EncryptedItemData for item_data when creating a PublicItem!")
        
        else:
            return self.vault_data.create_public_item(
                name=name,
                note=note,
                item_data=item_data
            )
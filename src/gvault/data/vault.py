from gvault.data import item

class VaultData:
    def __init__(self, encryption_key: bytes | None = None):
        self.private_items: list[item.PrivateItem] = []
        self.public_items: list[item.PublicItem] = []
        
        self.encryption_key: bytes | None = encryption_key
        
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            # NOTE NEVER-EVER-EVER INCLUDE self.encryption_key EVER!
            "private": [item.to_dict(convert_bytes_to_hex) for item in self.private_items],
            "public": [item.to_dict(convert_bytes_to_hex) for item in self.public_items]
        }
    
    
    def set_encryption_key(self, key: bytes):
        self.encryption_key = key
    
    
    def get_items_by_name(self, name: str) -> list[item.PrivateItem | item.PublicItem]:
        _name = name.lower()
        return self.get_private_items_by_name(name=_name) + self.get_public_items_by_name(name=_name)
    
    
    def get_public_items_by_name(self, name: str) -> list[item.PublicItem]:
        _name = name.lower()
        
        return [item.name.lower() == _name and item for item in self.public_items]
    
    
    def get_private_items_by_name(self, name: str) -> list[item.PrivateItem]:
        _name = name.lower()
        
        return [item.name.lower() == _name and item for item in self.private_items]
    
    
    def create_public_item(self, name: str, note: str, item_data: item.AccountItemData | item.FileItemData | item.NoteItemData) -> item.PublicItem:
        new_public_item = item.PublicItem(
            name=name,
            note=note,
            item_data=item_data
        )
        
        self.public_items.append(new_public_item)
        
        return new_public_item

    
    def create_private_item(self, name: str, note: str, item_data: item.EncryptedItemData | item.FileItemData | item.NoteItemData, encrypt_on_create: bool | None = False) -> item.PrivateItem:
        new_private_item = item.PrivateItem(
            name=name,
            note=note,
            item_data=item_data
        )
        
        if encrypt_on_create:
            if not self.encryption_key:
                raise Exception("Cannot decrypt a private item without an encryption key!")
            
            new_private_item.encrypt(self.encryption_key)
        
        self.private_items.append(new_private_item)
        
        return new_private_item
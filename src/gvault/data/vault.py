

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
    
    
    def get_items_by_name(self, name: str) -> list[item.PrivateItem | item.PublicItem]:
        _name = name.lower()
        return [
            item.name.lower() == _name and item for item in self.public_items
        ] + [
            item.name.lower() == _name and item for item in self.private_items
        ]
    
    
    def get_public_items_by_name(self, name: str) -> list[item.PublicItem]:
        _name = name.lower()
        
        return [item.name.lower() == _name and item for item in self.public_items]
    
    
    def get_private_items_by_name(self, name: str) -> list[item.PrivateItem]:
        _name = name.lower()
        
        return [item.name.lower() == _name and item for item in self.private_items]
    
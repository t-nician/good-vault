from object import entry, hash


class VaultObject:
    def __init__(self):
        self.public: list[entry.PublicEntryObject] = []
        self.private: list[entry.PrivateEntryObject] = []
        
    
    def create_private_entry(
        self,
        password: str,
        name: str, 
        type: str,
        data: dict | list | str,
        note: str | None = "",
    ) -> entry.PrivateEntryObject:
        _hash = hash.ScryptObject()
        _hash.remember_password(password)
        
        new_entry = entry.PrivateEntryObject(
            name=name,
            entry_type=type,
            note=note,
            data=data,
            hash=_hash  
        ) 
        
        self.private.append(new_entry)
        
        return new_entry
    
    
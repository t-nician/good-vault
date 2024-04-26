import json


from gvault.data import entry, hash


class AccountData:
    def __init__(self):
        self.private_entries: list[entry.PrivateEntry] = []
        self.public_entries: list[entry.PublicEntry] = []
        
        self.hash: hash.ScryptHashData = hash.ScryptHashData()
        
        self.password: str | None = None
        self.authorization_key: str | None = None
        
    
    def get_entry_by_uuid(self, uuid: str) -> entry.PrivateEntry | entry.PublicEntry | None:
        for entry in self.private_entries:
            if entry.uuid == uuid:
                return entry
        
        for entry in self.public_entries:
            if entry.uuid == uuid:
                return entry
    
    
    
    
    
import json


from gvault.data import entry


class AccountData:
    def __init__(self):
        self.private_entries: list[entry.PrivateEntry] = []
        self.public_entries: list[entry.PublicEntry] = []
        
    
    def get_entry_by_uuid(self, uuid: str) -> entry.PrivateEntry | entry.PublicEntry | None:
        for entry in self.private_entries:
            if entry.uuid == uuid:
                return entry
        
        for entry in self.public_entries:
            if entry.uuid == uuid:
                return entry
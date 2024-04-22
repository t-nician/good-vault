DEFAULT_SALT_LENGTH = 32
DEFAULT_HASH_LENGTH = 32

DEFAULT_SCRYPT_N = 2 ** 14
DEFAULT_SCRYPT_R = 8
DEFAULT_SCRYPT_P = 1


import uuid


class ScryptData:
    def __init__(
        self, 
        salt_length: int = DEFAULT_SALT_LENGTH, 
        hash_length: int = DEFAULT_HASH_LENGTH, 
        N: int = DEFAULT_SCRYPT_N, 
        r: int = DEFAULT_SCRYPT_R, 
        p: int = DEFAULT_SCRYPT_P
    ):
        self.salt_length = salt_length
        self.hash_length = hash_length
        
        self.param_n = N
        self.param_r = r
        self.param_p = p
    

class EntryData:
    def __init__(self, name: str, uuid: str, data: str, note: str = ""):
        self.name = name
        self.uuid = uuid
        
        self.data = data
        
        self.note = note


class VaultData:
    def __init__(self):
        self.entries: list[EntryData] = []
    
    
    def get_entry_by_uuid(self, uuid: str) -> EntryData | None:
        for entry in self.entries:
            if entry.uuid == uuid:
                return entry
            
    
    def get_entries_by_note(self, note: str) -> list[EntryData]:
        results = []
        
        for entry in self.entries:
            if entry.note == note:
                results.append(entry)
        
        return results
    
    
    def get_entries_by_name(self, name: str) -> list[EntryData]:
        results = []
        
        for entry in self.entries:
            if entry.name == name:
                results.append(entry)
        
        return results
    
    
    def get_entries_by_name_and_note(self, name: str, note: str) -> list[EntryData]:
        results = []
        
        for entry in self.entries:
            if entry.name == name and entry.note == note:
                results.append(entry)
        
        return results
    

    def add_entry(self, name: str, data: str, note: str = "", uuid: str = uuid.uuid4().hex) -> EntryData:
        new_entry = EntryData(
            name=name,
            data=data,
            note=note,
            uuid=uuid
        )
        
        self.entries.append(new_entry)
        
        return new_entry
    
    


class AccountData:
    def __init__(self):
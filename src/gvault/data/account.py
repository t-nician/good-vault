import json


from Crypto.Cipher import AES
from gvault.data import entry, hash


class AccountData:
    def __init__(self, password: str | None = None, salt: bytes | None = None, authorization_key: bytes | None = None):
        self.private_entries: list[entry.PrivateEntry] = []
        self.public_entries: list[entry.PublicEntry] = []
        
        self.hash: hash.ScryptHashData = hash.ScryptHashData(
            salt=salt
        )
        
        self.password: str | None = password
        self.authorization_key: bytes | None = authorization_key or password and self.hash.get_authorization_key(password) or None
                
    
    def login(self, password: str) -> bool:
        
        if self.authorization_key == self.hash.get_authorization_key(password):
            self.password = password
            return True

        return False
    
    
    def get_entry_by_uuid(self, uuid: str) -> entry.PrivateEntry | entry.PublicEntry | None:
        for entry in self.private_entries:
            if entry.uuid == uuid:
                return entry
        
        for entry in self.public_entries:
            if entry.uuid == uuid:
                return entry
    
    
    def create_public_entry(self, name: str, note: str, data: entry.AccountEntryData | entry.FileEntryData | entry.NoteEntryData) -> entry.PublicEntry:
        new_public_entry = entry.PublicEntry(
            name=name,
            note=note,
            data=data
        )
        
        self.public_entries.append(new_public_entry)
        
        return new_public_entry

    
    def create_private_entry(self, name: str, note: str, data:  entry.AccountEntryData | entry.FileEntryData | entry.NoteEntryData, password: str | None = None) -> entry.PrivateEntry:
        if not self.login(password or self.password):
            raise Exception("Passwords do not match!")
        
        _password = password or self.password
        _prepared_data = data.to_bytes()
        
        _cipher = AES.new(
            key=self.hash.get_encryption_key(_password),
            mode=AES.MODE_EAX
        )
        
        new_private_entry = entry.PrivateEntry(
            name=name,
            type=data.type,
            note=note,
            nonce=_cipher.nonce,
            data=_cipher.encrypt(_prepared_data)
        )
        
        self.private_entries.append(new_private_entry)
        
        return new_private_entry
    
    
    def private_entries_to_dict(self) -> list[dict]:
        entries = []
        
        for entry in self.private_entries:
            entries.append(entry.to_dict())
        
        return entries
    
    
    def public_entries_to_dict(self) -> list[dict]:
        entries = []
        
        for entry in self.public_entries:
            entries.append(entry.to_dict())
        
        return entries
    
    
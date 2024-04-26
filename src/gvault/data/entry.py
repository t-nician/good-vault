import json, enum

from Crypto.Cipher import AES


class DataEntryType(enum.StrEnum):
    ACCOUNT = "ACCOUNT"
    FILE = "FILE"
    NOTE = "NOTE"


class BaseEntryData:
    def __init__(self):
        self.type: DataEntryType
        
    def to_bytes(self) -> bytes:
        return b''


class AccountEntryData:
    def __init__(self, username: str, password: str, website: str | None = ""):
        self.username = username
        self.password = password
        self.website = website
        
        self.type = DataEntryType.ACCOUNT

    
    def to_bytes(self) -> bytes:
        return json.dumps({
            "username": self.username,
            "password": self.password,
            "website": self.website
        }).encode()


class FileEntryData:
    def __init__(self, data: bytes):
        self.data = data
        
        self.type = DataEntryType.FILE
    
    
    def to_bytes(self) -> bytes:
        return self.data


class NoteEntryData:
    def __init__(self, note: str):
        self.note = note
        
        self.type = DataEntryType.NOTE
    
    
    def to_bytes(self) -> bytes:
        return self.note.encode()


class PrivateEntry:
    def __init__(self, name: str, type: DataEntryType, note: str, nonce: bytes, data: bytes):
        self.name = name
        self.note = note
        self.type = type
        
        self.nonce = nonce
        self.data = data
    
    
    def to_entry_data(self, decryption_key: bytes) -> BaseEntryData:
        _data = AES.new(
            key=decryption_key, 
            nonce=self.nonce, 
            mode=AES.MODE_EAX
        ).decrypt(self.data)
        
        
        if self.type == DataEntryType.ACCOUNT:
            _data = json.loads(_data)
            
            return AccountEntryData(
                username=_data["username"],
                password=_data["password"],
                website=_data["website"]
            )


class PublicEntry:
    def __init__(self, name: str, note: str, data: BaseEntryData):
        self.name = name
        self.note = note
        self.data = data
    
    
    def to_private_entry(self, encryption_key: bytes) -> PrivateEntry:
        _data = self.data.to_bytes()
        _cipher = AES.new(key=encryption_key, mode=AES.MODE_EAX)
        
        return PrivateEntry(
            name=self.name,
            type=self.data.type,
            note=self.note,
            nonce=_cipher.nonce,
            data=_cipher.encrypt(_data)
        )
        
        
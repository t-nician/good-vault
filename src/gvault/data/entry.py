import json, enum


class DataEntryType(enum.StrEnum):
    ACCOUNT = "ACCOUNT"
    FILE = "FILE"
    NOTE = "NOTE"


class BaseEntryData:
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
        })


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



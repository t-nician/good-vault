import enum, json

from Crypto.Cipher import AES


class EntryDataType(enum.StrEnum):
    ACCOUNT = "ACCOUNT"
    NOTE = "NOTE"
    FILE = "FILE"


class BaseEntryData:
    def __get_prepped_data_for_encryption(self) -> bytes:
        return b''
    
    
    def __call__(self) -> bytes:
        return self.__get_prepped_data_for_encryption()


class AccountEntryData(BaseEntryData):
    def __init__(self, username: str, password: str, website: str | None = ""):
        self.username = username
        self.password = password
        self.website = website
    
    
    def __get_prepped_data_for_encryption(self) -> bytes:
        return json.dumps({
            "username": self.username,
            "password": self.password,
            "website": self.website
        }).encode()
    

class NoteEntryData(BaseEntryData):
    def __init__(self, note: str):
        self.note = note
        
    
    def __get_prepped_data_for_encryption(self) -> bytes:
        return self.note.encode()


class FileEntryData(BaseEntryData):
    def __init__(self, data: bytes):
        self.data = data
        
    
    def __get_prepped_data_for_encryption(self) -> bytes:
        return self.data
        

class PrivateEntry:
    def __init__(self, name: str, type: EntryDataType, nonce: bytes, data: bytes, note: str | None = ""):
        self.name = name
        self.type = type
        self.note = note
        
        self.nonce = nonce
        self.data = data        


class PublicEntry:
    def __init__(self, name: str, type: EntryDataType, data: BaseEntryData, note: str| None = ""):
        self.name = name
        self.note = note
        self.type = type
        self.data = data
    
    
    def create_encrypted_entry(self, encryption_key: bytes) -> PrivateEntry:
        _data = self.data()
        _cipher = AES.new(
            key=encryption_key,
            mode=AES.MODE_EAX
        )
        
        return PrivateEntry(
            name=self.name,
            note=self.note,
            type=self.type,
            nonce=_cipher.nonce,
            data=_cipher.encrypt(_data)
        )
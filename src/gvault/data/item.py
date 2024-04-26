import enum, json, uuid

from Crypto.Cipher import AES


DEFAULT_AES_MODE = AES.MODE_EAX

class ItemVisibility(enum.StrEnum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"

class ItemDataType(enum.StrEnum):
    ENCRYPTED = "encrypted"
    ACCOUNT = "account"
    FILE = "file"
    NOTE = "note"


class AccountItemData:
    def __init__(self, username: str, password: str, website: str):
        self.type = ItemDataType.ACCOUNT
        
        self.username = username
        self.password = password
        self.website = website
    
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "website": self.website,
            "type": str(ItemDataType.ACCOUNT)
        }


class FileItemData:
    def __init__(self, name: str, data: bytes):
        self.type = ItemDataType.FILE
        
        self.name = name
        self.data = data
    
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            "name": self.name,
            "data": self.data,
            "type": str(ItemDataType.FILE)
        }


class NoteItemData:
    def __init__(self, note: str):
        self.type = ItemDataType.NOTE
        
        self.note = note
        
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            "note": self.note,
            "type": str(ItemDataType.NOTE)
        }


class EncryptedItemData:
    def __init__(self, nonce: bytes, data: bytes, real_type: ItemDataType | None = None):
        self.type = ItemDataType.ENCRYPTED
        self.real_type = real_type
        
        self.nonce = nonce
        self.data = data
    
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            "type": str(self.type),
            "real_type": str(self.real_type),
            "nonce": convert_bytes_to_hex and self.nonce.hex() or self.nonce,
            "data": convert_bytes_to_hex and self.data.hex() or self.data
        }


class PrivateItem:
    def __init__(self, name: str, note: str, item_data: EncryptedItemData | AccountItemData | FileItemData | NoteItemData):
        self.name = name
        self.note = note
        
        self.item_data = item_data
        
        self.is_public = False
        self.is_decrypted = type(item_data) is not EncryptedItemData
        
        self.uuid = uuid.uuid4().hex
    
    
    def decrypt(self, decryption_key: bytes):
        if self.is_decrypted:
            return None


        _cipher = AES.new(key=decryption_key, nonce=self.item_data.nonce, mode=DEFAULT_AES_MODE)
        _decrypted_data = _cipher.decrypt(self.item_data.data)
        
        _decrypted_dict = json.loads(_decrypted_data)
        _item_data_type = ItemDataType(_decrypted_dict["type"])
        
        del _decrypted_dict["type"]
        
        if _item_data_type is ItemDataType.ACCOUNT:
            self.item_data = AccountItemData(
                **_decrypted_dict
            )
        elif _item_data_type is ItemDataType.FILE:
            self.item_data = FileItemData(
                **_decrypted_dict
            )
        elif _item_data_type is ItemDataType.NOTE:
            self.item_data = NoteItemData(
                **_decrypted_dict
            )
        
    
    def encrypt(self, encryption_key: bytes):
        if not self.is_decrypted:
            return None
        
        
        _cipher = AES.new(key=encryption_key, mode=DEFAULT_AES_MODE)
        _encrypted_data = _cipher.encrypt(
            json.dumps(self.item_data.to_dict(False)).encode()
        )
        
        new_item_data = EncryptedItemData(
            _cipher.nonce,
            _encrypted_data,
            self.item_data.type,
        )
        
        self.item_data = new_item_data
        self.is_decrypted = False
        
    
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            "name": self.name,
            "note": self.note,
            
            "data": self.item_data.to_dict(convert_bytes_to_hex)
        }


class PublicItem:
    def __init__(self, name: str, note: str, item_data: AccountItemData | FileItemData | NoteItemData):
        self.name = name
        self.note = note
        
        self.item_data = item_data
        
        self.is_public = True
        self.uuid = uuid.uuid4().hex
    
    
    def to_dict(self, convert_bytes_to_hex: bool | None = False) -> dict:
        return {
            "name": self.name,
            "note": self.note,
            
            "data": self.item_data.to_dict(convert_bytes_to_hex)
        }

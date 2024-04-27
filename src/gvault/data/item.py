import enum
import json

from Crypto.Cipher import AES

class ItemDataType(enum.StrEnum):
    ENCRYPTED = "encrypted"
    ACCOUNT = "account"
    MESSAGE = "message"
    FILE = "file"


class ItemScopeType(enum.StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class EncryptedItemData:
    def __init__(self, type: ItemDataType, nonce: bytes, data: bytes):
        self.type = type
        
        self.nonce = nonce
        self.data = data
    
    
    def to_dict(self, bytes_to_hex: bool | None = False):
        return {
            "nonce": bytes_to_hex and self.nonce.hex() or self.nonce,
            "data": bytes_to_hex and self.data.hex() or self.data
        }


class AccountItemData:
    def __init__(self, username: str, password: str, website: str):
        self.type = ItemDataType.ACCOUNT
        
        self.username = username
        self.password = password
        self.website = website
    
    
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "website": self.website
        }


class MessageItemData:
    def __init__(self, name: str, message: str):
        self.type = ItemDataType.MESSAGE
        
        self.name = name
        self.message = message
        
    
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        return {
            "name": self.name,
            "message": self.message
        }


class FileItemData:
    def __init__(self, name: str, data: bytes):
        self.type = ItemDataType.FILE
        
        self.name = name
        self.data = data
    
    
    def to_dict(self, bytes_to_hex: bool | None = False):
        return {
            "name": self.name,
            "data": bytes_to_hex and self.data.hex() or self.data
        }


def unpack_dict_to_item_data(
    type: ItemDataType, data: dict
) -> EncryptedItemData | AccountItemData | MessageItemData | FileItemData:
    if type is ItemDataType.ENCRYPTED:
        return EncryptedItemData(**data)
    elif type is ItemDataType.ACCOUNT:
        return AccountItemData(**data)
    elif type is ItemDataType.MESSAGE:
        return MessageItemData(**data)
    elif type is ItemDataType.FILE:
        return FileItemData(**data)


class PrivateItem:
    def __init__(
        self, item_name: str, item_note: str, item_data: EncryptedItemData 
                                                            | AccountItemData 
                                                            | MessageItemData 
                                                            | FileItemData,
        encrypt_on_create: bool | None = False,
        decrypt_on_create: bool | None = False,
        key: bytes | None = None
    ):
        self.item_scope = ItemScopeType.PRIVATE
        
        self.item_name = item_name
        self.item_note = item_note
        
        self.item_data = item_data
        
        if encrypt_on_create or decrypt_on_create:
            if not key:
                raise Exception(
                    "Cannot encrypt or decrypt on create without a key!"
                )

            if encrypt_on_create and decrypt_on_create:
                raise Exception("Cannot encrypt and decrypt at the same time!")
            
            if encrypt_on_create:
                self.encrypt(key)
            elif decrypt_on_create:
                self.decrypt(key)
    
    
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        return {
            "name": self.item_name,
            "note": self.item_note,
            "type": str(self.item_data.type),
            
            "data": self.item_data.to_dict(bytes_to_hex)
        }

    
    def decrypt(self, decryption_key: bytes):
        if type(self.item_data) is EncryptedItemData:
            _type = self.item_data.type
            _data = json.loads(AES.new(
                key=decryption_key, 
                nonce=self.item_data.nonce, 
                mode=AES.MODE_EAX
            ).decrypt(self.item_data.data))
            
            self.item_data = unpack_dict_to_item_data(
                type=_type,
                data=_data
            )
        else:
            raise Exception("Can't decrypt an already decrypted item!")
    
    
    def encrypt(self, encryption_key: bytes):
        if type(self.item_data) is not EncryptedItemData:
            cipher = AES.new(key=encryption_key, mode=AES.MODE_EAX)
            self.item_data = EncryptedItemData(
                type=self.item_data.type,
                nonce=cipher.nonce,
                data=cipher.encrypt(
                    json.dumps(
                        self.item_data.to_dict(bytes_to_hex=True)
                    ).encode()
                )
            )
        else:
            raise Exception("Can't encrypt an already encrypted item!")
        

class PublicItem:
    def __init__(
        self, item_name: str, item_note: str, item_data: AccountItemData 
                                                            | MessageItemData 
                                                            | FileItemData
    ):
        self.scope = ItemScopeType.PUBLIC
        
        self.item_name = item_name
        self.item_note = item_note
        
        self.item_data = item_data
    
    
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        return {
            "name": self.item_name,
            "note": self.item_note,
            "type": str(self.item_data.type),
            
            "data": self.item_data.to_dict(bytes_to_hex)
        }
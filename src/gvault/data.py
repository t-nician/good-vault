import json
import uuid
import dataclasses


from gvault import base

from Crypto.Cipher import AES


@dataclasses.dataclass
class BaseItemData(base.BaseFunctions):
    uuid: str = base.data_field(
        save=True, encrypt=False, default_factory=lambda: uuid.uuid4().hex
    )


@dataclasses.dataclass
class AccountItemData(BaseItemData):
    username: str = base.data_field(save=True, encrypt=False, default="")
    password: str = base.data_field(save=True, encrypt=True, default="")
    website: str = base.data_field(save=True, encrypt=False, default="")


@dataclasses.dataclass
class NoteItemData(BaseItemData):
    name: str = base.data_field(save=True, encrypt=False, default="")
    content: str = base.data_field(save=True, encrypt=True, default="")


@dataclasses.dataclass
class EncryptedItemField(BaseItemData):
    name: str = base.data_field(save=True, encrypt=False, default="")
    
    data: bytes = base.data_field(save=True, encrypt=False, default=b"")
    nonce: bytes = base.data_field(save=True, encrypt=False, default=b"")
    

@dataclasses.dataclass
class EncryptedItemData(BaseItemData):
    encrypted_item_fields: list[EncryptedItemField] = base.data_field(
        save=True, encrypt=False, default_factory=list
    )

    decrypted_item_data: AccountItemData | NoteItemData = base.data_field(
        save=True, encrypt=False, default_factory=BaseItemData
    )


@dataclasses.dataclass
class VaultItem(base.BaseFunctions):
    name: str = base.data_field(save=True, encrypt=False, default="")
    note: str = base.data_field(save=True, encrypt=False, default="")
    
    item_data: EncryptedItemData | AccountItemData | NoteItemData = base.data_field(
        save=True, encrypt=False, default_factory=BaseItemData
    )
    
    __is_encrypted: bool = base.data_field(
        save=False, encrypt=False, default=False
    )
    
    def __post_init__(self):
        if type(self.item_data) is EncryptedItemData:
            self.__is_encrypted = True
    
    
    def encrypt_item(self, key: bytes):
        if self.__is_encrypted:
            return None

        encrypted_item_fields = []
        
        for field in dataclasses.fields(self.item_data):
            if field.metadata["save"] and field.metadata["encrypt"]:
                
                data = getattr(self.item_data, field.name, "")
                data_type = type(data)
                
                if data_type is str:
                    data = data.encode()
                elif data_type is list or data_type is dict:
                    data = json.dumps(data).encode()
                elif callable(getattr(data, "to_json", None)):
                    data = data.to_json(bytes_to_hex=False).encode()

                cipher = AES.new(key=key, mode=AES.MODE_EAX)
                nonce = cipher.nonce
                
                encrypted_data = cipher.encrypt(data)
                
                encrypted_field = EncryptedItemField(
                    name=field.name,
                    data=encrypted_data,
                    nonce=nonce
                )
                
                encrypted_item_fields.append(encrypted_field)
            elif field.metadata["save"]:
                
                
    
    
    def decrypt_item(self, key: bytes):
        pass
    

@dataclasses.dataclass
class VaultData(base.BaseFunctions):
    vault_items: list[VaultItem] = base.data_field(
        save=True, encrypt=False, default_factory=list
    )
    
    
    
    
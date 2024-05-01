import json
import dataclasses

from gvault import tool
from gvault.data import entry


from Crypto.Cipher import AES


DEFAULT_KEY_CHECK_DATA = b"success"


@dataclasses.dataclass
class VaultEntryData(tool.DataToDictHandler):
    entry_data: entry.BaseEntryData | entry.EncryptedEntryData | entry.AccountEntryData | entry.FileEntryData | entry.NoteEntryData = dataclasses.field(
        metadata={"save": True},
        default_factory=entry.BaseEntryData
    )
    
    def encrypt_entry_data(self, key: bytes):
        if type(self.entry_data) is entry.EncryptedEntryData:
            raise Exception("Cannot encrypt an already encrypted entry!")
        
        cipher = AES.new(key=key, mode=AES.MODE_EAX)
        
        result = self.entry_data.to_encrypt_and_not_encrypt_dicts(
            bytes_to_hex=True
        )
        
        encrypt_dict = result[0]
        decrypt_dict = result[1]
        
        encrypted_data = cipher.encrypt(json.dumps(encrypt_dict).encode())
        
        encrypted_entry_data = entry.EncryptedEntryData(
            encrypted_type=self.entry_data.entry_type,
            
            encryption_nonce=cipher.nonce,
            encrypted_data=encrypted_data,
            
            decrypted_data=decrypt_dict,
        )
        
        self.entry_data = encrypted_entry_data
    
    
    def decrypt_entry_data(self, key: bytes):
        if type(self.entry_data) is not entry.EncryptedEntryData:
            raise Exception("Entry data is already decrypted!")

        cipher = AES.new(
            key=key, 
            nonce=self.entry_data.encryption_nonce,
            mode=AES.MODE_EAX
        )
        
        


@dataclasses.dataclass
class VaultData(tool.DataToDictHandler):
    """VaultData

    encrypted_entries:\n       save: True
    
    decrypted_entries:\n       save: True
    
    key_check_data:\n       save: True
    
    key_check_nonce:\n       save: True
    
    __vault_key:\n       save: False
    """
    encrypted_entries: list[entry.EncryptedEntryData] = dataclasses.field(
        metadata={"save": True},
        default_factory=list
    )
    
    decrypted_entries: list[
        entry.AccountEntryData
        | entry.FileEntryData
        | entry.NoteEntryData
    ] = dataclasses.field(
        metadata={"save": True},
        default_factory=list
    )
    
    key_check_data: bytes | None = dataclasses.field(
        metadata={"save": True},
        default=None
    )
    
    key_check_nonce: bytes | None = dataclasses.field(
        metadata={"save": True},
        default=None
    )
    
    __vault_key: bytes | None = dataclasses.field(
        metadata={"save": False},
        default=None
    )
    
    def assign_vault_key(self, key: bytes) -> bool:
        
        cipher = AES.new(
            key=key, 
            nonce=self.key_check_nonce, 
            mode=AES.MODE_EAX
        ) 
        
        if self.key_check_data is None:
            if self.key_check_nonce is not None:
                raise Exception(
                    "VaultData creation failure! key_check_data but no nonce!"
                )
            
            self.key_check_data = cipher.encrypt(DEFAULT_KEY_CHECK_DATA)
            self.key_check_nonce = cipher.nonce
            
            self.__vault_key = key
            
            return True
        
        
        if cipher.decrypt(self.key_check_data) == DEFAULT_KEY_CHECK_DATA:
            self.__vault_key = key
            return True
        
        return False
    
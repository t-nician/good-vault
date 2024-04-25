DEFAULT_SCRYPT_LENGTH = 32
DEFAULT_SCRYPT_N = 16384
DEFAULT_SCRYPT_R = 8
DEFAULT_SCRYPT_P = 1

_type = type

import json

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

from Crypto.Random import get_random_bytes


class PrivateEntryObject:
    def __init__(self, name: str, type: str, note: str, nonce: bytes | str | None = None, data: str | bytes | None = None):
        self.name: str = name
        self.type: str = type
        
        self.note: str  = note
        
        self.nonce: bytes = _type(nonce) is str and bytes.fromhex(nonce)
        self.data: bytes = _type(data) is str and bytes.fromhex(data)
    
    
    def get_decrypted_data(self, decryption_key: bytes) -> bytes:
        return AES.new(key=decryption_key, nonce=self.nonce, mode=AES.MODE_EAX).decrypt(self.data)
    
    
    def update_data(self, encryption_key: bytes, data: bytes):
        cipher = AES.new(key=encryption_key, mode=AES.MODE_EAX)
            
        self.nonce = cipher.nonce
        self.data = cipher.encrypt(data)
        
    

class PublicEntryObject:
    def __init__(self, name: str, type: str, data: str | bytes | list | dict, note: str):
        self.name: str = name
        self.type: str = type
        self.data: str | bytes | list | dict = data
        self.note: str  = note
    

class VaultObject:
    def __init__(self):
        self.private: list[PrivateEntryObject] = []
        self.public: list[PublicEntryObject] = []
   
    
    def create_private_entry(
        self,
        encryption_key: bytes,
        name: str,
        type: str,
        data: str | bytes | list | dict,
        note: str | None = ""
    ) -> PrivateEntryObject:
        _prepped_data = b''
        
        if _type(data) is str:
            _prepped_data = data.encode()
        elif not _type(data) is bytes:
            _prepped_data = json.loads(data).encode()
        
        new_entry = PrivateEntryObject(
            name=name,
            type=type,
            note=note
        )
        
        new_entry.update_data(
            encryption_key=encryption_key, 
            data=_prepped_data
        )
        
        return new_entry
        
    
    def create_public_entry(
        self,
        name: str,
        type: str,
        data: str | bytes | list | dict,
        note: str | None = ""
    ) -> PublicEntryObject:
        new_entry = PublicEntryObject(
            name=name,
            type=type,
            data=data,
            note=note
        )
        
        self.public.append(new_entry)
        
        return new_entry


class ScryptObject:
    def __init__(
        self,
        salt_override: bytes | None = None,
        length: int | None = DEFAULT_SCRYPT_LENGTH,
        N: int | None = DEFAULT_SCRYPT_N,
        r: int | None = DEFAULT_SCRYPT_R,
        p: int | None = DEFAULT_SCRYPT_P,
    ):
        self.salt = salt_override or get_random_bytes(length)
        self.length = length
        self.N = N
        self.r = r
        self.p = p
    
    
    def new_salt(self):
        self.salt = get_random_bytes(self.length)
    
    
    def get_authorization_key(self, password: str) -> bytes:
        return self.__generic_hash(password, num_keys=1)
        
    
    def get_encryption_key(self, password: str) -> bytes:
        return self.__generic_hash(password, num_keys=2)[1]
    
    
    def __generic_hash(self, password: str, num_keys: int | None = 1) -> bytes | list[bytes]:
        return scrypt(
            password=password,
            salt=self.salt,
            key_len=self.length,
            N=self.N,
            r=self.r,
            p=self.p,
            num_keys=num_keys
        )


class AccountObject:
    def __init__(
        self, 
        username: str | None = None,
        vault_override: VaultObject | None = VaultObject(),
        scrypt_override: ScryptObject | None = ScryptObject(),
        authorization_key_override: bytes | None = None,
        
    ):
        self.vault: VaultObject = vault_override
        self.scrypt: ScryptObject = scrypt_override
        
        self.username: str | None = username
        
        self.authorization_key: bytes | None = authorization_key_override
        
        
    def authorize(self, password: str) -> bool:
        return self.scrypt.get_authorization_key(password) == self.authorization_key
    
    
    def update_password(self, old_password: str, new_password: str):
        if self.authorization_key is None or self.authorize(old_password):
            
            self.__override_password(new_password)
            
            # TODO talk to self.vault and update encrypted data!
            # NOTE check if self.authorization_key exists, if not start an initialization with new_password!
    
    
    def __override_password(self, password: str):
        self.scrypt.new_salt()
        
        self.authorization_key = self.scrypt.get_authorization_key(password)

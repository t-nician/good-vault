import uuid
import dataclasses

from Crypto.Cipher import AES


@dataclasses.dataclass
class VaultField:
    name: str = dataclasses.field(default="")
    note: str = dataclasses.field(default="")
    data: str | bytes = dataclasses.field(default="")
    nonce: str | bytes = dataclasses.field(default="")
    
    is_encrypted: bool = dataclasses.field(default=False)
    
    encrypt_field: bool = dataclasses.field(default=False)
    save_field: bool = dataclasses.field(default=False)
    
    def __post_init__(self):
        if len(self.nonce) > 0:
            self.is_encrypted = True
    
    
    def encrypt(self, key: bytes, bytes_to_hex: bool | None = False):
        if self.is_encrypted:
            return None
        
        cipher = AES.new(key=key, mode=AES.MODE_EAX)
        
        prepped_data = self.data
        prepped_nonce = cipher.nonce
        
        if type(prepped_data) is str:
            prepped_data = prepped_data.encode()
            
        encrypted_data = cipher.encrypt(prepped_data)
        
        self.is_encrypted = True
        
        self.data = bytes_to_hex and encrypted_data.hex() or encrypted_data
        self.nonce = bytes_to_hex and prepped_nonce.hex() or prepped_nonce
    
    
    def decrypt(self, key: bytes):
        if not self.is_encrypted:
            return None
        
        prepped_nonce = self.nonce
        prepped_data = self.data
        
        if type(prepped_nonce) is str:
            prepped_nonce = bytes.fromhex(prepped_nonce)
            
        if type(prepped_data) is str:
            prepped_data = bytes.fromhex(prepped_data)
        
        cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=prepped_nonce)
        decrypted_data = cipher.decrypt(prepped_data)
        
        try:
            decrypted_data = decrypted_data.decode()
        except:
            pass
        
        self.is_encrypted = False
        
        self.data = decrypted_data
        self.nonce = ""
    

@dataclasses.dataclass
class BaseData:
    uuid: str = dataclasses.field(default_factory=lambda: uuid.uuid4().hex)


@dataclasses.dataclass
class AccountData(BaseData):
    username: VaultField = dataclasses.field(
        default_factory=lambda: VaultField(
            name="username",
             
            save_field=True,
            encrypt_field=False
        )
    )
    
    password: VaultField = dataclasses.field(
        default_factory=lambda: VaultField(
            name="password",
             
            save_field=True,
            encrypt_field=True
        )
    )
    
    website: VaultField = dataclasses.field(
        default_factory=lambda: VaultField(
            name="website",
             
            save_field=True,
            encrypt_field=False
        )
    )
    
    
@dataclasses.dataclass
class NoteData(BaseData):
    title: VaultField = dataclasses.field(
        default_factory=VaultField(
            name="title",
             
            save_field=True,
            encrypt_field=False
        )
    )
    
    content: VaultField = dataclasses.field(
        default_factory=VaultField(
            name="content",
             
            save_field=True,
            encrypt_field=True
        )
    )


class VaultData:
    vault_data: list[BaseData] = dataclasses.field(default_factory=list)
    vault_key: bytes = dataclasses.field(default=b"")
    
    
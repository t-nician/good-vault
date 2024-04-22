import json, enum

from core import secure

SALT_LENGTH = 32
HASH_LENGTH = 32

SCRYPT_N = 2 ** 14
SCRYPT_R = 8
SCRYPT_P = 1


class ScryptInformation:
    def __init__(
        self, 
        
        salt: str | bytes | None = None,
        
        salt_length: int | None = SALT_LENGTH,
        hash_length: int | None = HASH_LENGTH,
        
        scrypt_n: int | None = SCRYPT_N,
        scrypt_r: int | None = SCRYPT_R,
        scrypt_p: int | None = SCRYPT_P
    ):
        self.salt = type(salt) is str and bytes.fromhex(salt) or (salt or secure.get_random_bytes(salt_length))
        
        self.salt_length = salt_length
        self.hash_length = hash_length
        
        self.scrypt_n = scrypt_n
        self.scrypt_r = scrypt_r
        self.scrypt_p = scrypt_p


    def refresh_salt(self):
        self.salt = secure.get_random_bytes(self.salt_length)
        
        
    def get_authorization_key(self, password: str) -> bytes:
        return secure.hash_password(
            password=password,
            salt = self.salt,
            hash_length=self.hash_length,
            hash_count=1,
            N=self.scrypt_n,
            r=self.scrypt_r,
            p=self.scrypt_p
        )
        
        
    def get_encryption_key(self, password: str) -> bytes:
        return secure.hash_password(
            password=password,
            salt = self.salt,
            hash_length=self.hash_length,
            hash_count=2,
            N=self.scrypt_n,
            r=self.scrypt_r,
            p=self.scrypt_p
        )[1]


class EntryType(enum.StrEnum):
    ACCOUNT = "ACCOUNT"
    NOTE = "NOTE"
    MISC = "MISC"

class EntryInformation:
    pass


class DecryptedVaultInformation:
    def __init__(self, vault_data: dict | None = None):
        self.vault_entries: list[EntryInformation] = vault_data and vault_data.get("entries") or []
    
    
    def add_entry(self, name: str, type: EntryType, website: str, data: dict):
        self.vault_entries.append(
            EntryInformation()
        )
        

class VaultInformation:
    def __init__(self, vault_data: str | bytes = b'', vault_nonce: str | bytes = b''):
        self.vault_data = type(vault_data) is str and bytes.fromhex(vault_data) or vault_data
        self.vault_nonce = type(vault_nonce) is str and bytes.fromhex(vault_nonce) or vault_nonce
        
    
    def is_empty(self) -> bool:
        return self.vault_data == b'' or self.vault_nonce == b''
    
    
    def decrypt_vault(self, key: bytes) -> DecryptedVaultInformation | None:
        if self.is_empty():
            return DecryptedVaultInformation()
        
        result = secure.decrypt_data(key=key, nonce=self.vault_nonce, data=self.vault_data)
        
        if result:
            return DecryptedVaultInformation(
                json.loads(result)
            )
    
    
    def update_and_encrypt_vault(self, key: bytes, data: DecryptedVaultInformation | bytes):
        _target_data: bytes = type(data) is bytes and data or None
        
        if not _target_data:
            _target_data = json.dumps({
                "entries": data.vault_entries
            }).encode()
        

        self.vault_data, self.vault_nonce = secure.encrypt_data(key=key, data=_target_data)

class AccountInformation:
    def __init__(self, account_username: str, account_email: str = ""):
        self.account_username = account_username
        self.account_username = account_email
        
    
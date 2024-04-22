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


class VaultInformation:
    def __init__(self, vault_data: str | bytes, vault_nonce: str | bytes):
        self.vault_data = type(vault_data) is str and bytes.fromhex(vault_data) or vault_data
        self.vault_nonce = type(vault_nonce) is str and bytes.fromhex(vault_nonce) or vault_nonce


class AccountInformation:
    def __init__(self, account_username: str, account_email: str = ""):
        self.account_username = account_username
        self.account_username = account_email
        
    
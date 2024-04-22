import json

from database import model, secure


class AccountHandler:
    def __init__(self, account_model: model.Account, account_password: str = None, initialize_account: bool = False):
        self.account_model = account_model
        
        self.account_username = account_model.username
        self.account_email = account_model.email

        if initialize_account and account_password:
            self.__initialize_account(account_password)
    

    def decrypt_vault(password: str) -> dict:
        pass


    def __initialize_account(self, password: str):
        hashes, salt = secure.hash_password(password, 2)

        authorization_key, encryption_key = hashes[0], hashes[1]

        encrypted_vault, vault_nonce = secure.encrypt_data(encryption_key, b"{}")

        self.account_model.password = authorization_key.hex()
        self.account_model.vault = json.dumps({
            "data": encrypted_vault.hex(),
            "nonce": vault_nonce.hex()
        })

        self.account_model.scrypt = json.dumps({
            "salt": salt.hex(),
            "hash_length": secure.BASE_HASH_LENGTH,
            "salt_length": secure.BASE_SALT_LENGTH,
            "N": secure.BASE_HASH_N,
            "r": secure.BASE_HASH_R,
            "p": secure.BASE_HASH_P
        })

        self.account_model.entries = "[]"

        self.account_model.save()



from database import model, secure


class AccountHandler:
    def __init__(self, account_model: model.Account, account_password: str = None, initialize_account: bool = False):
        self.account_model = account_model
        
        self.account_username = account_model.username
        self.account_email = account_model.email

        if initialize_account and account_password:
            self.__initialize_account(account_password)
    

    def __initialize_account(self, password: str):
        hashes = secure.hash_password(password, 2)

        authorization_key, encryption_key = hashes[0], hashes[1]

        encrypted_vault, vault_nonce = secure.encrypt_data(encryption_key, "{}")

        self.account_model.password = authorization_key.hex()



import json

from database import model, secure


class AccountHandler:
    def __init__(self, account_model: model.Account, account_password: str = None, initialize_account: bool = False):
        self.account_model = account_model
        
        self.account_username = account_model.username
        self.account_email = account_model.email
        self.account_scrypt = {}
        self.account_vault = {}

        if initialize_account and account_password:
            self.__initialize_account(account_password)
        else:
            self.account_scrypt = json.loads(self.account_model.scrypt)
            self.account_vault = json.loads(self.account_model.vault)
    

    def update_password(self, original_password: str, new_password: str):
        original_hashes, original_salt = secure.hash_password(
            password=original_password,
            hashes=2,
            salt=bytes.fromhex(self.account_scrypt.get("salt"))
        )

        if original_hashes[0] == bytes.fromhex(self.account_model.password):
            decrypted_vault_data = secure.decrypt_data(
                key=original_hashes[1],
                nonce=bytes.fromhex(self.account_vault.get("nonce")),
                data=bytes.fromhex(self.account_vault.get("data"))
            )
            

            new_hashes, new_salt = secure.hash_password(
                password=new_password,
                hashes=2
            )

            encrypted_vault_data, new_nonce = secure.encrypt_data(
                key=new_hashes[1],
                data=decrypted_vault_data
            )

            self.account_model.password = new_hashes[0].hex()

            self.account_scrypt["salt"] = new_salt.hex()

            self.account_vault["data"] = encrypted_vault_data.hex()
            self.account_vault["nonce"] = new_nonce.hex()

            self.account_model.scrypt = json.dumps(self.account_scrypt)
            self.account_model.vault = json.dumps(self.account_vault)

            self.account_model.save()


    def decrypt_vault(self, password: str) -> dict:
        hashes, _ = secure.hash_password(
            password=password, 
            hashes=2, 
            salt=bytes.fromhex(self.account_scrypt.get("salt"))
        )

        if hashes[0] == bytes.fromhex(self.account_model.password):
            return json.loads(
                secure.decrypt_data(
                    key=hashes[1],
                    nonce=bytes.fromhex(self.account_vault.get("nonce")),
                    data=bytes.fromhex(self.account_vault.get("data"))
                )
            )


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



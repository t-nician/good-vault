import json

from gvault import data, model


def __dehex(target: dict):
    for (item, value) in target.items():
        if type(value) is str:
            try:
                target[item] = bytes.fromhex(value)
            except:
                pass
        elif type(value) is dict:
            __dehex(value)
        
        if type(item) is str:
            try:
                target[bytes.fromhex(item)] = value
                del target[item]
            except:
                pass
        elif type(item) is dict:
            __dehex(item)


def get_account_data_from_database(username: str, password: str | None = None, decrypt_private_data: bool | None = False) -> data.account.AccountData:
    account_model = model.get_account_model_by_username(username)
    
    if account_model:
        vault_data_dict = json.loads(account_model.vault_data)
        hash_data_dict = json.loads(account_model.hash_data)
        
        hash_data = None
        
        private_data = vault_data_dict["private"]
        public_data = vault_data_dict["public"]
        
        authorization_key = bytes.fromhex(account_model.authorization_key)
        
        if hash_data_dict["type"] == "scrypt":
            hash_data = data.hash.ScryptData(
                salt=bytes.fromhex(hash_data_dict["salt"]),
                length=hash_data_dict["length"],
                N=hash_data_dict["N"],
                r=hash_data_dict["r"],
                p=hash_data_dict["p"]
            )
        
        account_data = data.account.AccountData(
            username=username,
            password=password,
            hash_data=hash_data,
            authorization_key=authorization_key
        )
        
        for private_item in private_data:
            _type = data.item.ItemDataType(private_item["data"]["type"])
            _item_data = None
            
            print(_type, private_item)
            
            del private_item["data"]["type"]
            
            if _type is data.item.ItemDataType.ENCRYPTED:
                _item_data = data.item.EncryptedItemData(**private_item["data"])
            elif _type is data.item.ItemDataType.ACCOUNT:
                _item_data = data.item.AccountItemData(**private_item["data"])
            elif _type is data.item.ItemDataType.FILE:
                _item_data = data.item.FileItemData(**private_data)
            elif _type is data.item.ItemDataType.NOTE:
                _item_data = data.item.NoteItemData(**private_item)
            
            account_data.create_item(
                name=pri
            )
        

def save_account_data_to_database(account_data: data.account.AccountData):
    if not account_data.is_logged_in:
        raise Exception("Account must be logged in to save to database!")
    
    
    for private_item in account_data.vault_data.private_items:
        private_item.encrypt(account_data.encryption_key)
        
    
    account_model = model.get_account_model_by_username(account_data.username) or model.create_account_model(account_data.username)
    
    account_model.authorization_key = account_data.authorization_key.hex()
    
    account_model.hash_data = json.dumps(account_data.hash_data.to_dict(convert_bytes_to_hex=True))
    account_model.vault_data = json.dumps(account_data.vault_data.to_dict(convert_bytes_to_hex=True))
    
    account_model.save()
        
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
            __dehex(private_item)
            
            _type = data.item.ItemDataType(private_item["data"]["type"])
            _real_type = data.item.ItemDataType(private_item["data"]["real_type"])
            
            _item_data = None
            
            del private_item["data"]["type"]
            del private_item["data"]["real_type"]
            
            if _type is data.item.ItemDataType.ENCRYPTED:
                _item_data = data.item.EncryptedItemData(**private_item["data"], real_type=_real_type)
            elif _type is data.item.ItemDataType.ACCOUNT:
                _item_data = data.item.AccountItemData(**private_item["data"])
            elif _type is data.item.ItemDataType.FILE:
                _item_data = data.item.FileItemData(**private_data["data"])
            elif _type is data.item.ItemDataType.NOTE:
                _item_data = data.item.NoteItemData(**private_item["data"])
            
            account_data.create_item(
                name=private_item["name"],
                note=private_item["note"],
                item_data=_item_data,
                visibility=data.item.ItemVisibility.PRIVATE,
                encrypt_on_create=False
            )


        for public_item in public_data:
            __dehex(public_item)
            
            _type = data.item.ItemDataType(public_item["data"]["type"])
            
            _item_data = None
            
            del public_item["data"]["type"]
            
            if _type is data.item.ItemDataType.ACCOUNT:
                _item_data = data.item.AccountItemData(**public_item["data"])
            elif _type is data.item.ItemDataType.FILE:
                _item_data = data.item.FileItemData(**public_item["data"])
            elif _type is data.item.ItemDataType.NOTE:
                _item_data = data.item.NoteItemData(**public_item["data"])
                
            account_data.create_item(
                name=public_item["name"],
                note=public_item["note"],
                item_data=_item_data,
                visibility=data.item.ItemVisibility.PUBLIC
            )
            
        return account_data
        

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
        
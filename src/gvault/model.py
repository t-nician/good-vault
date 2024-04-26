import peewee, json

from gvault.data import account, entry, hash

database = peewee.SqliteDatabase(":memory:")


class BaseModel(peewee.Model):
    class Meta:
        database = database


class AccountModel(BaseModel):
    username = peewee.TextField(unique=True, index=True)
    
    auth = peewee.TextField()
    hash = peewee.TextField()
    
    public = peewee.TextField()
    private = peewee.TextField()


def __dehex_dict(target: dict):
    for (item, value) in target.items():
        if type(item) is dict:
            __dehex_dict(item)
        
        if type(value) is dict:
            __dehex_dict(value)
        
        if type(item) is str:
            try:
                target[bytes.fromhex(item)] = value
                target[item] = None
            except:
                pass
        
        if type(value) is str:
            try:
                target[item] = bytes.fromhex(value)
            except:
                pass


def get_account_model_by_username(username: str) -> AccountModel | None:
    result = None
    
    try:
        result = AccountModel.get(
            AccountModel.username==username
        )
    except Exception as _:
        pass
    
    return result


def get_account_data(username: str) -> account.AccountData | None:
    result = get_account_model_by_username(username)
    
    
    if result is not None:
        private_data = json.loads(result.private)
        public_data = json.loads(result.public)
        
        hash_data = json.loads(result.hash)
        auth_key = bytes.fromhex(result.auth)
        
        __dehex_dict(hash_data)
        
        for private_entry in private_data:
            __dehex_dict(private_entry)
            
        for public_entry in public_data:
            __dehex_dict(public_entry)
            
        new_account = account.AccountData(
            authorization_key=auth_key,
            hash_data_override=hash.ScryptHashData(
                salt=hash_data["salt"],
                length=hash_data["length"],
                N=hash_data["N"],
                r=hash_data["r"],
                p=hash_data["p"]
            )
        )
        

        for private_entry in private_data:
            new_account.add_existing_private_entry(
                name=private_entry["name"],
                type=entry.EntryDataType(private_entry["type"]),
                note=private_entry["note"],
                nonce=private_entry["nonce"],
                data=private_entry["data"],
            )
        
        
        for public_entry in public_data:
            entry_type = entry.EntryDataType(public_entry["type"])
            entry_data = None
            
            if entry_type is entry.EntryDataType.ACCOUNT:
                entry_data = entry.AccountEntryData(
                    username=public_entry["data"]["username"],
                    password=public_entry["data"]["password"],
                    website=public_entry["data"]["website"]
                )
            elif entry_type is entry.EntryDataType.FILE:
                entry_data = entry.FileEntryData(
                    name=public_entry["data"]["name"],
                    data=public_entry["data"]["data"]
                )
            elif entry_type is entry.EntryDataType.NOTE:
                entry_data = entry.NoteEntryData(
                    note=public_entry["data"]["note"]
                )
            
            new_account.create_public_entry(
                name=public_entry["name"],
                note=public_entry["note"],
                data=entry_data
            )
        
        return new_account


def save_account_data(username: str, account_data: account.AccountData):
    private_data = json.dumps(account_data.private_entries_to_dict(True))
    public_data = json.dumps(account_data.public_entries_to_dict(True))
    
    hash_data = json.dumps(account_data.hash.to_dict(True))
    
    authorization_key = account_data.authorization_key.hex()
    
    account_model = get_account_model_by_username(username) or AccountModel.create(
        username=username,
        auth=authorization_key,
        hash=hash_data,
        private=private_data,
        public=public_data
    )
    
    account_model.save()


TARGET_TABLES = [AccountModel]

for table in TARGET_TABLES:
    if not database.table_exists(table):
        database.create_tables([table])
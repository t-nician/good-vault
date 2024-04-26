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
        
        if type(item) is bytes:
            target[bytes.fromhex(item)] = value
            target[item] = None
        
        if type(value) is bytes:
            target[item] = bytes.fromhex(value)


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
        private_data = result.private
        public_data = result.public
        
        hash_data = result.hash
        auth_key = bytes.fromhex(result.auth)


def save_account_data(username: str, account_data: account.AccountData):
    private_data = json.dumps(account_data.private_entries_to_dict())
    public_data = json.dumps(account_data.public_entries_to_dict())
    
    hash_data = json.dumps(account_data.hash.to_dict(True))
    
    authorization_key = account_data.authorization_key.hex()
    
    
    
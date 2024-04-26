import peewee, json


database = peewee.SqliteDatabase(":memory:")


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
                

class BaseModel(peewee.Model):
    class Meta:
        database = database


class AccountModel(BaseModel):
    username = peewee.TextField(unique=True, index=True)
    
    hash_data = peewee.TextField()
    vault_data = peewee.TextField()
    
    authorization_key = peewee.TextField()


def get_account_model_by_username(username: str) -> AccountModel | None:
    result: None | AccountModel = None
    
    try:
        result = AccountModel.get(
            AccountModel.username == username
        )
    except:
        pass
    
    return result


TARGET_TABLES = [AccountModel]


for table in TARGET_TABLES:
    if not database.table_exists(table):
        database.create_tables([table])
import peewee, json


database = peewee.SqliteDatabase(":memory:")
                

class BaseModel(peewee.Model):
    class Meta:
        database = database


class AccountModel(BaseModel):
    username = peewee.TextField(unique=True, index=True)
    
    hash_data = peewee.TextField(default="")
    vault_data = peewee.TextField(default="")
    
    authorization_key = peewee.TextField(default="")


def get_account_model_by_username(username: str) -> AccountModel | None:
    result: None | AccountModel = None
    
    try:
        result = AccountModel.get(
            AccountModel.username == username
        )
    except:
        pass
    
    return result


def create_account_model(username: str) -> AccountModel | None:
    if get_account_model_by_username(username):
        return None
    
    return AccountModel.create(
        username=username
    )


TARGET_TABLES = [AccountModel]


for table in TARGET_TABLES:
    if not database.table_exists(table):
        database.create_tables([table])
import peewee


database = peewee.SqliteDatabase("workspace/database.sqlite")


class BaseModel(peewee.Model):
    class Meta:
        database = database
    

class AccountModel(BaseModel):
    username = peewee.TextField(unique=True, index=True)
    
    email = peewee.TextField(default="")
    authorization_key = peewee.TextField(default="")
    
    hash = peewee.TextField(default="")
    vault_id = peewee.TextField(default="")


class VaultModel(BaseModel):
    id = peewee.TextField(unique=True, index=True)
    
    private = peewee.TextField(default="")
    public = peewee.TextField(default="")


def try_get_account_model_by_username(username: str) -> AccountModel | None:
    result = None
    
    try:
        result = AccountModel.get(
            AccountModel.username == username
        )
    except:
        pass
    
    return result


def try_get_vault_model_by_id(id: str) -> VaultModel | None:
    result = None
    
    try:
        result = VaultModel.get(
            VaultModel.id == id
        )
    except:
        pass
    
    return result


TARGET_MODELS = [AccountModel, VaultModel]


for model in TARGET_MODELS:
    if not database.table_exists(model):
        database.create_tables([model])
import peewee


database = peewee.SqliteDatabase("workspace/database.sqlite")


class BaseModel(peewee.Model):
    class Meta:
        database = database
    

class AccountModel(BaseModel):
    username = peewee.TextField(unique=True, index=True, primary_key=True)
    
    email = peewee.TextField(default="")
    authorization_key = peewee.TextField(default="")
    
    hash = peewee.TextField(default="")
    
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


TARGET_MODELS = [AccountModel]


for model in TARGET_MODELS:
    if not database.table_exists(model):
        database.create_tables([model])

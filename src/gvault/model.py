import peewee

database = peewee.SqliteDatabase(":memory:")


class BaseModel(peewee.Model):
    class Meta:
        database = database


class AccountModel(BaseModel):
    username = peewee.TextField(unique=True, index=True)
    
    auth = peewee.TextField()
    salt = peewee.TextField()
    
    public = peewee.TextField()
    private = peewee.TextField()
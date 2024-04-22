import peewee


database_connection = peewee.SqliteDatabase("./workspace/database.sqlite")
database_connection.connect()


class BaseModel(peewee.Model):
    class Meta:
        database = database_connection


class Account(BaseModel):
    username = peewee.TextField(index=True, primary_key=True, unique=True)
    password = peewee.TextField(null=True, default="")
    email = peewee.TextField(null=True, default="")

    # { salt: str, hash_length: int, salt_length: int, N: int, r: int, p: int }
    scrypt = peewee.TextField(null=True, default="")

    # { data: str, nonce: str }
    vault = peewee.TextField(null=True, default="")

    # [ { name: str, uuid: str, type: str } ]
    entries = peewee.TextField(null=True, default="")


if not database_connection.table_exists(Account):
    database_connection.create_tables([Account])


database_connection.commit()
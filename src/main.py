import object

account = object.account.AccountObject()

account.hash.remember_password("password")

entry: object.entry.PrivateEntryObject = account.vault.create_private_entry(
    "password",
    "name",
    "account",
    {"hello": "world!"},
    "note!"
)



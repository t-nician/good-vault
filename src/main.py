from gvault.data import account, vault, item

old_new_account = account.AccountData(
    "username",
    "password12345678"
)


new_account = account.AccountData(
    username="username",
    hash_data=old_new_account.hash_data,
    authorization_key=old_new_account.authorization_key
)

print("login success? ", new_account.login("password12345678"))
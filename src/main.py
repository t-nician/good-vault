from gvault.data import account, vault, item

new_account = account.AccountData(
    "username",
    "password12345678"
)

print(new_account.authorization_key)
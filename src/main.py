import gvault


account_a = gvault.data.account.AccountData(
    account_username="username",
    account_password="password"
)

account_b = gvault.data.account.AccountData(
    account_username="username",
    account_password="password",
    authorization_key=account_a.authorization_key,
    hash_data=account_a.hash_data
)

print(account_a.hash_data.salt)
print(account_b.hash_data.salt)
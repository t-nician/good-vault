from gvault.data import account, entry, hash

initiated_account = account.AccountData("password")
replicated_account = account.AccountData(salt=initiated_account.hash.salt, authorization_key=initiated_account.authorization_key)

print(replicated_account.login("password"))

new_private_entry = initiated_account.create_private_entry(
    name="test",
    note="note",
    data=entry.AccountEntryData(
        username="username",
        password="password",
        website=""
    )
)

print(initiated_account.private_entries_to_dict())
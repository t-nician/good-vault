from gvault import model
from gvault.data import account, entry, hash

created_account = account.AccountData("password")

created_account.create_private_entry(
    name="test",
    note="note",
    data=entry.AccountEntryData(
        username="username",
        password="password",
        website=""
    )
)

model.save_account_data("username", created_account)

retrieved_account = model.get_account_data("username")
encryption_key = retrieved_account.hash.get_encryption_key("password")
print("login success? ", retrieved_account.login("password"))

print(retrieved_account.get_private_entries_by_name("test")[0].to_entry_data(encryption_key).username)
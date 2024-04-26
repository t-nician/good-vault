from gvault import model
from gvault.data import account, entry, hash

created_account = account.AccountData("password")

created_account.create_public_entry(
    name="test",
    note="note",
    data=entry.AccountEntryData(
        username="username",
        password="password",
        website=""
    )
)

print(created_account.get_entries_by_name("test"))
model.save_account_data("username", created_account)

retrieved_account = model.get_account_data("username")
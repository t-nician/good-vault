from gvault import model
from gvault.data import account, entry, hash

initiated_account = account.AccountData("password")

new_private_entry = initiated_account.create_private_entry(
    name="test",
    note="note",
    data=entry.AccountEntryData(
        username="username",
        password="password",
        website=""
    )
)

model.save_account_data(initiated_account)
import gvault


public_entry = gvault.data.entry.PublicEntry(
    name="Hello",
    note="World",
    data=gvault.data.entry.AccountEntryData(
        username="username",
        password="password",
        website="N/A"
    )
)

private_entry = public_entry.to_private_entry(b'password12345678')

print(private_entry.to_entry_data(b'password12345678').username)
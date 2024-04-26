import gvault


public_entry = gvault.data.entry.PublicEntry(
    name="Hello",
    note="World",
    data=gvault.data.entry.AccountEntryData(
        username="username",
        password="password",
        website="website"
    )
)


# Convert a public entry to a private entry!
private_entry = public_entry.to_private_entry(b"password12345678")

# Grab and decrypt!
entry_data = private_entry.to_entry_data(b"password12345678")


if entry_data.type == gvault.data.entry.EntryDataType.ACCOUNT:
    print(entry_data.username, entry_data.password, entry_data.website)
    
elif entry_data.type == gvault.data.entry.EntryDataType.FILE:
    print(entry_data.name, entry_data.data)
    
elif entry_data.type == gvault.data.entry.EntryDataType.NOTE:
    print(entry_data.note)
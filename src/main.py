import gvault


public_entry = gvault.data.entry.PublicEntry(
    name="Hello",
    note="World",
    data=gvault.data.entry.FileEntryData(
        name="file.txt",
        data=b'file data'
    )
)


private_entry = public_entry.to_private_entry(b'password12345678')

print(private_entry.to_entry_data(b"password12345678").data)
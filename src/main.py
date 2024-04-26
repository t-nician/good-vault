import gvault


public_entry = gvault.data.entry.PublicEntry(
    name="Hello",
    note="World",
    data=gvault.data.entry.FileEntryData(
        name="file.txt",
        data=b'file data'
    )
)



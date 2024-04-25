import gvault


public_entry = gvault.data.entry.PublicEntry(
    "name",
    gvault.data.entry.EntryDataType.NOTE,
    gvault.data.entry.NoteEntryData("Note data"),
)

print(public_entry.create_encrypted_entry(b"password12345678").data)
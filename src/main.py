from gvault.data import vault, item

"""
account_vault = vault.VaultData()

account_vault.set_encryption_key(b"password12345678")

private_item = account_vault.create_private_item(
    name="Private Test Item",
    note="This is a private item!",
    item_data=item.AccountItemData(
        username="John Doe",
        password="password123",
        website="epic-website.com"
    ),
    encrypt_on_create=True
)

public_item = account_vault.create_public_item(
    name="Public Test Item",
    note="This is a public item!",
    item_data=item.NoteItemData(
        note="Hello there!"
    )
)

print(account_vault.to_dict(True))
"""
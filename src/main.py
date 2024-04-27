import gvault

vault = gvault.data.vault.VaultData(
    b"password12345678"
)

private_item = vault.create_private_item(
    item_name="Private Account",
    item_note="For a private website.",
    
    item_data=gvault.data.item.AccountItemData(
        username="Secret_John123",
        password="Password123",
        website="secret-website.com"
    ),
    
    encrypt_on_create=True
)

print(private_item.to_dict(True))
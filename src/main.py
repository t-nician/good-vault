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

public_item = vault.convert_private_item_to_public(private_item)
re_private_item = vault.convert_public_item_to_private(
    public_item, 
    True
)

print(re_private_item.to_dict(True))



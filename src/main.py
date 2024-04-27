import gvault

private_item = gvault.data.item.PrivateItem(
    item_name="Account Item",
    item_note="For a cool website!",
    
    item_data=gvault.data.item.AccountItemData(
        username="John_Doe123",
        password="Pass12345678",
        website="cool-guy.com"
    ),
    
    encrypt_on_create=True,
    key=b"password12345678"
)


print(private_item.to_dict(True))
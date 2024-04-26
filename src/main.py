from gvault.data import account, vault, item

new_account = account.AccountData(
    "username",
    "password12345678"
)

public_item: item.PublicItem = new_account.create_item(
    name="Public Item Name",
    note="Public Item Note",
    item_data=item.AccountItemData(
        username="John_Doe",
        password="password123",
        website="cool-website.com"
    ),
    visibility=item.ItemVisibility.PUBLIC
)

private_item: item.PrivateItem = new_account.create_item(
    name="Private Item Name",
    note="Private Item Note",
    item_data=item.NoteItemData(
        note="Hello there!"
    ),
    visibility=item.ItemVisibility.PRIVATE,
    encrypt_on_create=True
)

print(private_item.to_dict(True))

new_account.login("password12345678")

private_item.decrypt(new_account.encryption_key)

print(private_item.to_dict(True))
import gvault

from gvault.data import account, vault, item

new_account = account.AccountData(
    "username",
    "password12345678"
)

public_item: item.PrivateItem = new_account.create_item(
    name="Public Item Name",
    note="Public Item Note",
    item_data=item.AccountItemData(
        username="John_Doe",
        password="password123",
        website="cool-website.com"
    ),
    visibility=item.ItemVisibility.PRIVATE
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

gvault.save_account_data_to_database(new_account)

gvault.get_account_data_from_database("username")
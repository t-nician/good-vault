import gvault

from gvault.data import account, vault, item

account_data = account.AccountData(
    "username",
    "password"
)

private_item = account_data.create_item(
    name="item",
    note="note",
    item_data=item.AccountItemData(
        username="username",
        password="password",
        website="website"
    ),
    visibility=item.ItemVisibility.PRIVATE,
    encrypt_on_create=True
)

print(private_item.to_dict(True))
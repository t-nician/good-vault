from gvault.data import item

private_item = item.PrivateItem(
    "name",
    "note",
    item.AccountItemData(
        "username",
        "password",
        "website"
    )
)

private_item.encrypt(b"password12345678")
private_item.decrypt(b"password12345678")

print(private_item.item_data.username)
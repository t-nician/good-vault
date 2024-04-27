import gvault


account_a = gvault.data.account.AccountData(
    account_username="username",
    account_password="password"
)

account_a.vault_data.create_private_item(
    item_name="Cool Message",
    item_note="This is about something cool!",
    item_data=gvault.data.item.MessageItemData(
        name="Message Name",
        message="Message Content"
    )
)

account_a.vault_data.create_public_item(
    item_name="Announcement Message",
    item_note="This is a public announcement!",
    item_data=gvault.data.item.MessageItemData(
        name="Cool event soon!",
        message="A cool event is coming soon!"
    )
)

print("-"*50)
print(account_a.vault_data.to_dict(True, encrypt_private_items=False))
print("-"*50)
print(account_a.vault_data.to_dict(True, encrypt_private_items=True))
print("-"*50)
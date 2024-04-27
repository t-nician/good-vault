from gvault import server, data

#gvault.server.
#gvault.server.get_account_data_from_database_by_username("username")

account_data = data.account.AccountData(
    account_username="username",
    account_password="password"
)


account_data.vault_data.create_private_item(
    item_name="Secret Item",
    item_note="It's a secret, sssssh!",
    item_data=data.item.MessageItemData(
        name="Ultimate Bread Recipe",
        message="1 Loaf of Wonderbread"
    )
)


print("success?", server.save_account_data_to_database(account_data))

retrieved_account = server.get_account_data_from_database_by_username(
    "username"
)


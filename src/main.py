import database


account, message = database.try_get_account("username")

if not account:
    account, message = database.try_create_account("username", "password")


from database import handler, model


def try_get_account(username: str) -> tuple[handler.AccountHandler | None, str]:
    pass



def try_create_account(username: str, password: str, email: str = None) -> tuple[handler.AccountHandler | None, str]:
    if try_get_account(username)[0]:
        return None, "An account with that username already exists!"
    
    
    return handler.AccountHandler(
        account_model=model.Account.create(
            username=username,
            email = email
        ),
        account_password=password,
        initialize_account=True
    )
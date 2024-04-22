from database import handler, model


def try_get_account(username: str) -> tuple[handler.AccountHandler | None, str]:
    _account_model: model.Account | None = None

    try:
        _account_model = model.Account.get(
            model.Account.username==username
        )
    except Exception as _:
        pass

    if _account_model:
        return handler.AccountHandler(
            account_model=_account_model
        ), "Success!"
    
    return None, "No account found with that username!"


def try_create_account(username: str, password: str, email: str = "") -> tuple[handler.AccountHandler | None, str]:
    if try_get_account(username)[0]:
        return None, "An account with that username already exists!"
    
    
    return handler.AccountHandler(
        account_model=model.Account.create(
            username=username,
            email=email
        ),
        account_password=password,
        initialize_account=True
    ), "Success!"
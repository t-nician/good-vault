from database import model


class AccountHandler:
    def __init__(self, account_model: model.Account, account_password: str = None, initialize_account: bool = False):
        self.account_model = account_model
        
        self.account_username = account_model.username
        self.account_email = account_model.email

        if initialize_account and account_password:
            self.__initialize_account(account_password)
    

    def __initialize_account(self, password: str):
        pass
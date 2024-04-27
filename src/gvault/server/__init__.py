from gvault import data
from gvault.server import model, api


def get_account_data_from_database_by_username(
    self, username: str
) -> data.account.AccountData | None:
    pass
import json
import asyncio

from gvault import data
from gvault.server import model, api


def get_account_data_from_database_by_username(
    account_username: str,
    account_password: str | None = None,
) -> data.account.AccountData | None:
    account_dict = asyncio.run(
        api.get_account_by_username(account_username)
    )
    
    if not account_dict["success"]:
        return None
    
    print(account_dict)
    
    

def save_account_data_to_database(
    account_data: data.account.AccountData
) -> bool:
    vault_dict = account_data.vault_data.to_dict(True, True)
    hash_dict = account_data.hash_data.to_dict(True)
    
    return asyncio.run(
        api.create_account(
            username=account_data.account_username,
            email=account_data.account_email,
            
            authorization_key=account_data.authorization_key.hex(),
            
            hash=json.dumps(hash_dict),
            
            public=json.dumps(vault_dict["public_items"]),
            private=json.dumps(vault_dict["private_items"])
        )
    )["success"]
import gvault

vault = gvault.VaultManager()

vault.load_data_entries_from_list([
    {
        "type": "account",

        "website": {
            "save": True, "encrypt": False, 
            "data": "website", "nonce": "N/A"
        },

        "username": {
            "save": True, "encrypt": False, 
            "data": "username", "nonce": "N/A"
        },

        "password": {
            "save": True, "encrypt": True,
            "data": "encrypted_data", "nonce": "nonce_here"
        }
    }
])
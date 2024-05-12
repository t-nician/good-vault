import gvault

vault = gvault.core.data.VaultData()

vault.add_vault_data_from_dict({
        "type": "account",

        "website": {
            "save": True, "encrypt": False,
            "value": "website.com", "nonce": "n/a"
        },

        "username": {
            "save": True, "encrypt": False,
            "value": "username", "nonce": "n/a"
        },

        "password": {
            "save": True, "encrypt": True,
            "value": "asdgjiasdfpjioafsd", "nonce": "asdpoijasdfpijo"
        }
    })


print(vault.vault_data)
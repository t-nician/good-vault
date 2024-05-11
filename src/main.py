import gvault

vault = gvault.VaultManager()

vault.add_data_entry_from_dict({
    "type": "account",

    "website": {
        "save": True, "encrypt": False, "is_encrypted": False,
        "data": "website.com", "nonce": "N/A"
    },

    "username": {
        "save": True, "encrypt": False, "is_encrypted": False,
        "data": "website.com", "nonce": "N/A"
    },

    "password": {
        "save": True, "encrypt": True, "is_encrypted": False,
        "data": "password123", "nonce": "N/A"
    }
})

print(vault.data_entries)
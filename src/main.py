import manager

"""
    Entry Data:
        string - name
        string - uuid (NOTE unique)
        string - type
        string - note (NOTE optional)
        
        bytes/string - data (NOTE required, encrypted)
        bytes/string - nonce (NOTE required)
        
        
    Account Data:
        string - username (NOTE unique, index)
        string - password (NOTE hashed with scrypt)
        string - email (NOTE optional)
        
        json - scrypt:
            string - salt
            number - length
            number - param_n
            number - param_r
            number - param_p
        
        
        list[EntryData] - vault
"""

account = manager.account.AccountObject("username")

account.remember_password("password")

account.create_private_entry(
    name="entry", 
    type="account", 
    data={"username": "username", "password": "password"}
)

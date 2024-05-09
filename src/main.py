import gvault, dataclasses

account_data = gvault.data.AccountData()
account_data.password.data = "password!!!"

account_data.password.encrypt(b"password12345678")

print(account_data.password)

account_data.password.decrypt(b"password12345678")

print(account_data.password)
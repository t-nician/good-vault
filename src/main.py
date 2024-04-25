import data

account = data.object.AccountObject()
account.update_password("password", "password")

target_data = b'Hello world!'

entry = account.vault.create_private_entry(account.scrypt.get_encryption_key("password"), "test", "test", target_data)

print(entry.data)
print(entry.get_decrypted_data(account.scrypt.get_encryption_key("password")))
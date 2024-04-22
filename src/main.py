import core, database

scrypt_information = core.information.ScryptInformation()
vault_information = core.information.VaultInformation()


encryption_key = scrypt_information.get_authorization_key("password")

decrypted_vault = vault_information.decrypt_vault(encryption_key)
decrypted_vault.vault_entries.append("Hello")

vault_information.update_and_encrypt_vault(encryption_key, decrypted_vault)

print(vault_information.decrypt_vault(encryption_key).vault_entries)


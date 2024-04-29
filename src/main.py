import gvault

from Crypto.Random import get_random_bytes

encrypted_entry = gvault.data.entry.EncryptedEntryData(
    cipher_nonce=get_random_bytes(12),
    encrypted_data=b"encrypted data"
)

print(encrypted_entry.to_dict(True))
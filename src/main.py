from gvault.data.entry import *
from gvault.data.hash import *

public_entry = PublicEntry(
    name="name",
    note="note",
    data=AccountEntryData(
        username="username",
        password="password",
        website="website"
    )
)

test_hash = ScryptHashData()
print(test_hash.get_authorization_key("password12345678"))
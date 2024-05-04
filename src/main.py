import gvault

item_data = gvault.data.ItemData(
    name="name",
    note="note"
)

username_field = item_data.add_field(
    name="username",
    note="username-note",
    data="Epic_Username123"
)

password_field = item_data.add_field(
    name="password",
    note="password-note",
    data="Epic_Password123",
    
    do_i_encrypt=True,
    key=b"password12345678"
)

print(password_field)
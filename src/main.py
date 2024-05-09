import gvault, dataclasses

field = gvault.data.FieldData(
    field_name="username",
    field_note="account username",
    field_data="bruh"
)

field.encrypt(b"password12345678")

print(field)
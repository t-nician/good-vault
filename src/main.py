import gvault
import dataclasses

@gvault.util.vaultdata
class TestData:
    test_field = gvault.util.Field(save=True, encrypt=True)



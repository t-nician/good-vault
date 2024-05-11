import uuid
import dataclasses

from gvault import util
from Crypto.Cipher import AES

@util.vaultdata
class AccountData:
    website = util.Field(save=True)
    username = util.Field(save=True)

    password = util.Field(save=True, encrypt=True)

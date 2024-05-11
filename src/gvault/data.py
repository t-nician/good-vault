from gvault import util

@util.vault_data
class AccountData:
    type = "account"
    website = util.VaultField(save=True)
    username = util.VaultField(save=True)
    password = util.VaultField(save=True, encrypt=True)


@util.vault_data
class NoteData:
    type = "note"
    title = util.VaultField(save=True)
    content = util.VaultField(save=True, encrypt=True)



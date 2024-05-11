import dataclasses

@dataclasses.dataclass
class Field:
    data: str | bytes = dataclasses.field(default="")

    save: bool = dataclasses.field(default=False)
    encrypt: bool = dataclasses.field(default=False)


@dataclasses.dataclass
class VaultData:
    object: object


def vaultdata(object):

    @dataclasses.dataclass
    class WrappedVaultData:
        object = object

    return WrappedVaultData
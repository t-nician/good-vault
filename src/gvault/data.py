import json
import dataclasses

from gvault import base


@dataclasses.dataclass
class VaultData(base.ToDictToJSON):
    encrypted: list = base.base_field(
        save=True, 
        encrypt=False, 
        default_factory=list
    )
    
    decrypted: list = base.base_field(
        save=True,
        encrypt=False,
        default_factory=list
    )
    
    
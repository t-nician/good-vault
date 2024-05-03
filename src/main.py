import json
import dataclasses

import gvault

@dataclasses.dataclass
class TestData(gvault.base.BaseFunctions):
    dont_save: str = gvault.base.data_field(
        save=False, encrypt=False, default="no"
    )
    
    save_me: str = gvault.base.data_field(
        save=True, encrypt=False, default="save"
    )


@dataclasses.dataclass
class OtherData(gvault.base.BaseFunctions):
    data_list: list[TestData] = gvault.base.data_field(
        save=True, encrypt=False, default_factory=list
    )


test = OtherData()

test.data_list.append(TestData())

print(str(test))
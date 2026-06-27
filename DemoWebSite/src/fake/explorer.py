from model.explorer import Explorer
from typing import List

_explorers = [
    Explorer(name="Claude Hande",
        country="FR",
        description="Scarce during full moons"),
    Explorer(name="Noah Weiser",
        country="DE",
        description="Myopic machete man"),
]


def get_all() -> List[Explorer]:
    """return all explorers"""

    return _explorers

def get_one(name: str) -> Explorer | None:
    """return a specific explorer"""

    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    
    return None
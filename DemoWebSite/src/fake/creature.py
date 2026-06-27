from model.creature import Creature
from typing import List


_creatures = [
    Creature(
        name="Yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman"),
    Creature(
        name="Bigfoot",
        country="US",
        area="*",
        description="Yeti's Cousin Eddie",
        aka="Sasquatch"),
]


def get_all() -> List[Creature]:
    """return all Creatures"""

    return _creatures


def get_one(name: str) -> Creature | None:

    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    
    return None
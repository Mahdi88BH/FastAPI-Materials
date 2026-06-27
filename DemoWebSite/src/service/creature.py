from model.creature import Creature
import fake.creature as data
from typing import List, Optional


def get_all() -> List[Creature]:
    return data.get_all()


def get_one(name: str) -> Optional[Creature]:
    return data.get(name)

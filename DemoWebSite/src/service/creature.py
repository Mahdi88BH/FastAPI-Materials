from model.creature import Creature
import data.creature as data
from typing import List, Optional


def create(creature: Creature) -> Creature:
    return data.create(creature)

def get_all() -> List[Creature]:
    return data.get_all()


def get_one(name: str) -> Optional[Creature]:
    return data.get_one(name)

import os
from model.creature import Creature
# if os.getenv["CRYPTID_UNIT_TEST"]:
#     from fake import creature as data
# else:
#     from data import creature as data
from data import creature as data
from typing import List, Optional


def create(creature: Creature) -> Creature:
    return data.create(creature)


def get_all() -> List[Creature]:
    return data.get_all()


def get_one(name: str) -> Optional[Creature]:
    return data.get_one(name)


def modify(name: str, creature: Creature) -> Creature:
    return data.modify(name, creature)


def delete(name: str):
    return data.delete(name)
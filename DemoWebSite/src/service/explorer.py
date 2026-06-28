from model.explorer import Explorer
import data.explorer as data
from typing import List, Optional


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)

def get_all() -> List[Explorer]:
    return data.get_all()

def get_one(name: str) -> Optional[Explorer]:
    return data.get_one(name)
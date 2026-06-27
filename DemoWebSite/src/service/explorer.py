from model.explorer import Explorer
import fake.explorer as data
from typing import List, Optional


def get_all() -> List[Explorer]:
    return data.get_all()

def get_one(name: str) -> Optional[Explorer]:
    return data.get(name)
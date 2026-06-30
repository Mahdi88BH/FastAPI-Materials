from .init import curs, IntegrityError
from model.creature import Creature
from typing import List
from error import Duplicate, Missing


curs.execute("""create table if not exists creature(
            name text primary key, 
            description text, 
            country text, 
            area text, 
            aka text)""")


def row_to_model(row: tuple) -> Creature:
    
    name, description, country, area, aka = row
    return Creature(name=name, 
                    description=description, 
                    country=country, 
                    area=area, 
                    aka=aka)


def model_to_row(creature: Creature) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    qry = "select * from creature where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()

    if row:
        return row_to_model(row)
    else:
        raise Missing(msf=f"creature {name} not found")


def get_all() -> List[Creature]:
    qry = "select * from creature"
    curs.execute(qry) 

    return [row_to_model(row) for row in curs.fetchall()]


def create(creature: Creature) -> Creature:
    qry = """insert into creature
    values (:name, :description, :country, :area, :aka)"""
    params = model_to_row(creature)

    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"creature {creature.name} already exists")
    
    return get_one(curs.fetchone())


def modify(name: str, creature: Creature) -> Creature:
    if not (name and creature) : return None
    qry= """update creature
    set name:=name,
    description=:description,
    country=:country,
    area=:area,
    aka=:aka
    whara name=:origine_name"""
    params = model_to_row(creature)
    params["origine_name"] = creature.name
    curs.execute(qry, params)

    if curs.rowcount == 1:
        return get_one(creature.name)
    else:
        Missing(msg=f"creature {name} not found")


def delete(name: str):
    if not name : return False
    qry = """delete from creature where name=:name"""
    params = {"name": name}
    curs.execute(qry, params)

    if curs.rowcount != 1:
        Missing(msg=f"Creature {name} don't exists")
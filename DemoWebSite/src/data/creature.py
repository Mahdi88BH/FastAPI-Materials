from .init import conn, curs
from model.creature import Creature
from typing import List

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

    return row_to_model(curs.fetchone())

def get_all() -> List[Creature]:
    qry = "select * from creature"
    curs.execute(qry) 

    return [row_to_model(row) for row in curs.fetchall()]


def create(creature: Creature) -> Creature:
    qry = """insert into creature
    values (:name, :description, :country, :area, :aka)"""
    params = model_to_row(creature)
    curs.execute(qry, params)

    return get_one(curs.fetchone())


def modify(creature: Creature) -> Creature:
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

    return get_one(creature.name)


def replace(creature: Creature):

    return creature


def delete(creature: Creature) -> bool:
    qry = """delete from creature where name=:name"""
    params = {"name": creature.name}
    res = curs.execute(qry, params)

    return bool(res)
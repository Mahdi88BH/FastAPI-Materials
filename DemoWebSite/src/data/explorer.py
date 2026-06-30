from .init import (conn, curs, IntegrityError)
from model.explorer import Explorer
from typing import List
from error import Missing, Duplicate


curs.execute("""create table if not exists explorer(
            name text primary key,
            country text,
            description text)""")


def row_to_model(row: tuple) -> Explorer:
    name, country, description = row

    return Explorer(name=name, country=country, description=description)


def model_to_row(explorer: Explorer) -> dict:

    return explorer.model_dump() if explorer else None


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()

    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found") 


def get_all() -> List[Explorer]:
    qry = "select * from explorer"
    curs.execute(qry)

    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> Explorer:
    qry = """insert into explorer
    values(:name, :country, :description)"""
    params = model_to_row(explorer)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} alraed exist")

    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer): return None
    qry = """update explorer
    set name=:name,
    country=:country
    description=:description
    where name=:origine_name"""
    params = model_to_row(explorer)
    params["origine_name"] = explorer.name
    curs.execute(qry, params)

    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def delete(name: str):
    if not name: return False
    qry = "delete from explorer where name=:"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
    
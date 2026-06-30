from .init import curs, get_db, IntegrityError
from model.user import User
from error import Duplicate, Missing
from typing import List


curs.execute("""create table if not exists user(
            name text primary key,
            hash text)""")


curs.execute("""create table if not exists xuser(
            name text primary key,
            hash text)""")


def model_to_row(user: User) -> dict:
    return user.model_dump()


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name = name, hash = hash)

def get_one(name: str) -> User:
    qry="select * from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()

    if row:
        row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")


def get_all() -> List[User]:
    qry = "select * from user"
    curs.execute(qry)

    return [row_to_model(row) for row in curs.fetchall()]


def create(user: User, table: str = "user"):
    qry = f"""insert into {table}
    values (:name, :hash)"""
    params = model_to_row(user)

    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"user {user.name} already exists in table {table}")


def modify(name: str, user: User) -> User:
    qry = """update user set
    name=:name, hash=:hash
    whare name=:name0"""
    params = model_to_row(user)
    params["name0"] = name
    curs.execute(qry, user)

    if curs.rowcount == 1:
        return get_one(name)
    else:
        raise Missing(msg=f"User {name} not found")


def delete(name: str) -> None:
    user = get_one(name)
    qry="delete from user where name=:name"
    params = {"name" : name}
    curs.execute(qry, params)

    if curs.rowcount != 1:
        raise Missing(msg=f"user {name} not found")
    create(user, table="xuser")

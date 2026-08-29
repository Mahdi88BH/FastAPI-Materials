from datetime import date
from enum import Enum
from pydantic import BaseModel




class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: list[str]
    address: Address

    def name_dict(self):
        return self.model_dump(include={"first_name", "last_name"})


if __name__ == "__main__":

    person = Person(
                first_name="John",
                last_name="Doe",
                gender=Gender.MALE,
                birthdate="1991-01-01",
                interests=["travel", "sports"],
                address={
                    "street_address": "12 Squirell Street",
                    "postal_code": "424242",
                    "city": "Woodtown",
                    "country": "US",
                    }
                )

    # Converting an object into a dictionary
    person_dict = person.model_dump()

    print(person_dict["first_name"]) # "John"
    print(person_dict["address"]["street_address"]) # "12 Squirell Street"

    person_include = person.model_dump(include={"first_name", "last_name"})
    print(person_include) # {"first_name": "John","last_name": "Doe"}

    person_exclude = person.model_dump(exclude={"birthdate", "interests"})
    print(person_exclude)

    person_nested_include = person.dict( include={
        "first_name": ...,
        "last_name": ...,
        "address": {"city", "country"},
        }
    ) # {"first_name": "John", "last_name": "Doe", "address": {"city":"Woodtown", "country": "US"}}
    print(person_nested_include)

    print(person.name_dict())

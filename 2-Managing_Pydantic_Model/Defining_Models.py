from pydantic import BaseModel, ValidationError, Field, EmailStr, HttpUrl
from datetime import datetime
from datetime import date
from enum import Enum

# Don't assign a defualt value to model field becuase assign the value 
# once he instantiate

class Gender(str, Enum):
    MALE= "MALE"
    FEMALE= "FEMALE"


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


# Standard field types
class Person(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    age: int = Field(None, ge=0, lt=120)
    gender: Gender
    birthdate: date
    interests: list[str]
    address: Address
    location: str | None = None



def list_factory():
    return ['a', 'b', 'c']


class Model(BaseModel):
    l: list[str] = Field(default_factory=list_factory)
    d: datetime = Field(default_factory=datetime.now)
    l2: list[str] = Field(default_factory=list)


class User(BaseModel):
    email: EmailStr
    website: HttpUrl


if __name__ == "__main__":

    # Invalide Instantiation
    # try:
    #     Person(
    #         first_name="John",
    #         last_name="Doe",
    #         gender="INVALID_VALUE",
    #         birthdate="1991-01-01",
    #         interests=["travel", "sports"],
    #         )
    # except ValidationError as e:
    #     print(str(e))


    try:
        p = Person(
                first_name="John",
                last_name="Doe",
                # age=24, the value of age is Optional
                gender=Gender.MALE,
                birthdate="1991-01-01",
                interests=["travel", "sports"],
                address={
                    "street_address": "12 Squirell Street",
                    "postal_code": "424242",
                    "city": "Woodtown",
                    "country": "US",
                    },
                )
        
        print(p)
    except ValidationError as e:
        print(str(e))

    m = Model()
    print(m)

    user = User(
        email="elmahdibahadia_@gmail.com",
        website="https://www.example.com"
    )
        

    print(user)
    print(user.website.scheme)
    print(user.website.host)

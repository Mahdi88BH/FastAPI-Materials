from datetime import date
from pydantic import BaseModel, ValidationError, field_validator, EmailStr, model_validator


# Applying validation at the field level
class Person(BaseModel):
    first_name: str
    last_name: str
    birthdate: date

    @field_validator("birthdate")
    def valid_birthdate(cls, v: date):
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v



# Applying validation at the object level
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @model_validator(mode='after')
    def passwords_match(self) -> 'UserRegistration':
        if self.password != self.password_confirmation:
            raise ValueError("Passwords don't match")
        return self



# Applying validation before Pydantic parsing
class UserProfile(BaseModel):
    username: str
    age: int

    @model_validator(mode='before')
    @classmethod
    def clean_raw_input(cls, data: dict) -> dict:
        if isinstance(data, dict):
            # Clean up raw data before Pydantic tries to validate types
            if 'username' in data and isinstance(data['username'], str):
                data['username'] = data['username'].strip().lower()
        return data



if __name__ == "__main__":
    p = Person(
        first_name="John",
        last_name="Doe",
        birthdate="1991-01-01"
    )

    user = UserRegistration(
        email="Mahdi@gmail.com",
        password="Mahdi",
        password_confirmation="Mahdi"
    )

    userP = UserProfile(
        username="  MAHDI",
        age=32
    )

    print(p)
    print(user)
    print(userP)
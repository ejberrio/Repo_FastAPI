# Python
from dataclasses import field
from doctest import Example
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, EmailStr, PastDate
from pydantic import Field
from pydantic.types import PaymentCardNumber

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Nota: Correr con el servidor uvicorn (uvicorn main:app --reload)

# Models


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        ...,
        # example="Medellín"
    )
    state: str = Field(
        ...,
        # example="Antioquia"
    )
    country: str = Field(
        ...,
        # example="Colombia"
    )

    class Config:
        schema_extra = {
            "example": {
                "city": "Medellín",
                "state": "Antioquia",
                "country": "Colombia"
            }
        }


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(
        default=None
    )
    is_married: Optional[bool] = Field(
        default=None
    )
    email: Optional[EmailStr] = Field(
        default=None
    )
    birthday: Optional[PastDate] = Field(
        default="1989-05-12"
    )
    credit_card: Optional[PaymentCardNumber] = Field(
        default=None
    )


class Person(PersonBase):

    password: str = Field(
        ...,
        min_length=8
    )

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Lina",
                "last_name": "Corrales",
                "age": 34,
                "hair_color": "black",
                "is_married": True,
                "email": "linacorrales@gmail.com",
                "birthday": "1987-06-03",
                "credit_card": "376151292089510",
                "password": "holasoyever"
            }
        }


class PersonOut(PersonBase):
    pass


@app.get("/")
def home():
    return {"Hola": "mundo"}


# Request and response body

@app.post("/person/new", response_model=PersonOut)
def create_person(
    person: Person = Body(...)
):
    return person

# Validaciones: Query Parameters


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Lina"
    ),
    age: int = Query(
        ...,  # It's wear that way but it may be like that
        title="Person age",
        description="This is the person age. It's required",
        example=34
    )
):
    return {
        "name": name,
        "age": age
    }


# Validations: Path parameters

@app.get("/person/details/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person id",
        description="This is the person id. It's required and it must be greater than 0",
        example=10
    )
):
    return {person_id: "It exists"}


# Validations: Request Body (Personal training)

@app.put("/person/details/{person_id}")
def update_location(
    person_id: int = Path(
        ...,
        title="Person id",
        description="This is the person id",
        gt=0,
        example=10

    ),
    location: Location = Body(
        ...,
        title="Current person's location",
        description="Update the actual location of the person"
    )

):
    return location


# Validations: Request body

@ app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person id",
        description="This is the person id",
        gt=0,
        example=10
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())

    return results

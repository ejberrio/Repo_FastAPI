# Python
from ast import Return
import imp
from typing import Optional
from unittest import result

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Nota: Correr con el servidor uvicorn (uvicorn main:app --reload)

# Models


class Location(BaseModel):
    city: str
    state: str
    country: str


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"Hola": "mundo"}


# Request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters"
    ),
    age: int = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required"
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
        description="This is the person id. It's required and it must be greater than 0")
):
    return {person_id: "It exists"}


# Validations: Request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person id",
        description="This is the person id",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())

    return results

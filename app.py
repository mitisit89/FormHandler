import datetime
import re

import uvicorn
from fastapi import FastAPI, Query
from pydantic import (BaseModel, EmailStr, ValidationError, validate_email,
                      validator)
from tinydb import Query as db_q
from tinydb import TinyDB

app = FastAPI()
db = TinyDB("db.json")


class DateValidator(BaseModel):
    date: datetime.date

    @validator("date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()


class PhoneValidator(BaseModel):
    phone: str

    @validator("phone")
    def phone_validator(cls, value):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if value and not re.search(regex, value, re.I):
            raise ValueError("Phone Number Invalid.")
        return value


@app.post("/get_form")
async def get_form(query: list[str] = Query(default=[])):
    print(type(query[2].split("=")[1]))
    fields = {i.split("=")[0]: i.split("=")[1] for i in query}
    if (
        validate_email(query[0].split("=")[1])
        and DateValidator(date=query[2].split("=")[1])
        and PhoneValidator(phone=query[1].split("=")[1])
    ):
        print("email data phone")

    return 201


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

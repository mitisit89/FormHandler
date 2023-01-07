import datetime
import re

import uvicorn
from fastapi import FastAPI, Query
from tinydb import Query as db_query
from tinydb import TinyDB, where

app = FastAPI()
db = TinyDB("db.json")
forms = db.table("forms")


def date_validator(d: datetime) -> str:
    if datetime.datetime.strptime(d, "%Y-%m-%d").date():
        return "date"
    return


def phone_validator(phone: str) -> str:
    regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
    if phone and not re.search(regex, phone, re.I):
        print("Phone Number Invalid.")
    return "phone"


def mail_validator(email: str) -> str:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return "email"


def validator(form: dict) -> dict:
    __validate_form = {}
    for key, value in form.items():
        if value.startswith("+"):
            __validate_form[key] = phone_validator(value)
        elif "@" in value:
            __validate_form[key] = mail_validator(value)

        elif "-" in value:
            __validate_form[key] = date_validator(value)
        else:
            __validate_form[key] = "text"
    return __validate_form


@app.post("/get_form", status_code=201)
async def get_form(query: list[str] = Query(default=[])):
    form = {i.split("=")[0]: i.split("=")[1] for i in query}
    validate_form = validator(form)
    if form_name := forms.search(db_query().fragment(validate_form)):

        return form_name[0].get("name")
    else:
        return validate_form


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

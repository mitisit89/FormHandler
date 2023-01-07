import datetime
import re

import uvicorn
from fastapi import FastAPI, Query
from tinydb import Query as db_query
from tinydb import TinyDB

app = FastAPI()
db = TinyDB("db.json")
forms = db.table("forms")


def date_validator(d: datetime) -> str:
    try:
        if datetime.datetime.strptime(d, "%Y-%m-%d").date():
            return "date"
        return ""
    except ValueError as e:
        print(e)


def phone_validator(phone: str) -> str:
    regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
    if re.search(regex, phone, re.I):
        return "phone"
    return ""


def mail_validator(email: str) -> str:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return "email"
    return ""


def validator(form: dict) -> dict:
    validate_form = {}
    for key, value in form.items():
        if value.startswith("+"):
            validate_form[key] = phone_validator(value)
        elif "@" in value:
            validate_form[key] = mail_validator(value)

        elif "-" in value:
            validate_form[key] = date_validator(value)
        else:
            validate_form[key] = "text"
    return validate_form


@app.post("/get_form", status_code=201)
async def get_form(query: list[str] = Query(default=[])):
    form = {i.split("=")[0]: i.split("=")[1] for i in query}
    validate_form = validator(form)
    if form_name := forms.search(db_query().fragment(validate_form)):
        return form_name[0].get("name")
    elif "" in validate_form.values():
        return 400
    else:
        return validate_form


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

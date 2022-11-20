from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserInput(BaseModel):
    name: str
    surname: Optional[str]
    date_of_birth: Optional[date]
    interests: Optional[list[str]]


class TextInput(BaseModel):
    id: int
    message: str
    
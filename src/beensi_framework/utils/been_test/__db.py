from pydantic import BaseModel
from typing import Any


class DB(BaseModel):
    name: str
    description: str
    row: Any
    expected_result: Any

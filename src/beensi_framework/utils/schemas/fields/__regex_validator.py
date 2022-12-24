from pydantic import BaseModel


class RegExValidator(BaseModel):
    pattern: str
    error_messages: list

from pydantic import BaseModel as BModel
from typing import Optional


class MailSetting(BModel):
    USERNAME: Optional[str]
    PASSWORD: Optional[str]
    FROM: Optional[str]
    PORT: Optional[int]
    SERVER: Optional[str]
    FROM_NAME: Optional[str]

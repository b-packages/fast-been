from pydantic import BaseModel as BModel


class MailSetting(BModel):
    USERNAME: str
    PASSWORD: str
    FROM: str
    PORT: int
    SERVER: str
    FROM_NAME: str

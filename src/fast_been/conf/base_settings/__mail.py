from pydantic import BaseModel as BModel


class MailSetting(BModel):
    USERNAME: str
    PASSWORD: str
    FROM: str
    PORT: int = 587
    SERVER: str = 'smtp.gmail.com'
    FROM_NAME: str

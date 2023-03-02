from pydantic import BaseModel as BModel


class MailSetting(BModel):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = 'smtp.gmail.com'
    MAIL_FROM_NAME: str

from pydantic import BaseModel as BModel
from typing import Optional


class MailSetting(BModel):
    USERNAME: Optional[str] = 'nvd'
    PASSWORD: Optional[str] = '1234567890'
    FROM: Optional[str] = 'nvd@gmail.com'
    PORT: Optional[int] = '587'
    SERVER: Optional[str] = 'smtp.gmail.com'
    FROM_NAME: Optional[str] = 'beensi'

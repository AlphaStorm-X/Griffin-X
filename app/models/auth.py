from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class UserToken(Token):
    name: str
    email: EmailStr

class TokenData(BaseModel):
    username: Optional[str] = None

from pydantic import BaseModel, EmailStr


class UserBasicDTO(BaseModel):
    email: EmailStr
    password: str


class UserRegisterDTO(UserBasicDTO):
    username: str
    email: EmailStr
    password: str


class UserNotSensitiveDTO(BaseModel):
    username: str
    email: EmailStr

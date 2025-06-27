from pydantic import BaseModel


class LoginModel(BaseModel):
    email: str
    password: str


class RegisterModel(BaseModel):
    name: str
    email: str
    password: str


class BalanceModel(BaseModel):
    amount: float

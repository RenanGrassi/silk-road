from pydantic import BaseModel


class BaseDTO(BaseModel):
    group: str
    method: str

from pydantic import BaseModel


class BaseDTO(BaseModel):
    group: str
    method: str
    conf: dict | None = None

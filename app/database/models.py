from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    is_admin: bool
    username: str
    full_name: str
    timestamp: datetime

from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    is_admin: bool
    is_banned: bool
    username: Optional[str]
    full_name: Optional[str]
    timestamp: datetime

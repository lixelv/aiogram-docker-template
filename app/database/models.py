from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    username: Optional[str]
    full_name: Optional[str]
    language_code: Optional[str]
    timestamp: datetime

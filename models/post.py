from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    author: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

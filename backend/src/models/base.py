from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TimestampMixin(SQLModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
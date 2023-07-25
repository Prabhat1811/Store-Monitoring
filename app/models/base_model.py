import uuid
from typing import Optional
from sqlmodel import SQLModel
from sqlmodel import Field

class BaseModel(SQLModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)

    def __str__(self):
        return self.name

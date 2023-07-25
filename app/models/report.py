from datetime import datetime
from enum import Enum

from sqlmodel import Field

from .base_model import BaseModel


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Store_Status(BaseModel, table=True):
    store_id: str = Field(index=True)
    status: Status
    timestamp_utc: datetime


class Store_Timezone(BaseModel, table=True):
    store_id: str = Field(index=True)
    timezone: str


class Menu_Hours(BaseModel, table=True):
    store_id: str = Field(index=True)
    day: int = Field(ge=0, le=6)
    start_time_local: datetime
    end_time_local: datetime

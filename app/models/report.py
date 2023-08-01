from datetime import datetime, time
from enum import Enum

from sqlmodel import Field

from .base_model import BaseModel


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Store_Status(BaseModel, table=True):
    __tablename__ = "store_status"

    store_id: str =  Field(
        default=None, foreign_key="store_timezone.store_id", index=True
    )
    status: Status
    timestamp_utc: datetime

    def process_for_insert(self):
        self.status = self.status.value


class Store_Timezone(BaseModel, table=True):
    __tablename__ = "store_timezone"

    store_id: str = Field(index=True)
    timezone: str

    def process_for_insert(self):
        pass


class Menu_Hours(BaseModel, table=True):
    __tablename__ = "menu_hours"

    store_id: str = Field(
        default=None, foreign_key="store_timezone.store_id", index=True
    )
    day: int = Field(ge=0, le=6)
    start_time_local: time
    end_time_local: time

    def process_for_insert(self):
        pass

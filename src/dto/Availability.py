from datetime import datetime
from pydantic import BaseModel

class AvailabilityDTO(BaseModel):
    date: datetime
    slots: list[int]
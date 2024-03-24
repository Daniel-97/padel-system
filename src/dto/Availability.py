from datetime import datetime
from pydantic import BaseModel

class AvailabilityDTO(BaseModel):
    date: datetime
    start_hour: int
    end_hour: int
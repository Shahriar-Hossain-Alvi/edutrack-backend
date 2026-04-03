from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NotificationBaseSchema(BaseModel):
    message: str
    # title: str
    user_id: int


class NotificationResponseSchema(NotificationBaseSchema):
    id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

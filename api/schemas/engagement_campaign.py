from pydantic import BaseModel
from datetime import datetime

# Base schema for engagement campaign data
class EngagementCampaignBase(BaseModel):
    title: str
    description: str
    status: str
    start_date: datetime
    end_date: datetime

# Schema for creating an engagement campaign
class EngagementCampaignCreate(EngagementCampaignBase):
    pass

# Schema for outputting engagement campaign details
class EngagementCampaignOut(EngagementCampaignBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

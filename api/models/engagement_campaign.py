from sqlalchemy import Column, Integer, String, Text, DateTime
from ..dependencies.database import Base
from datetime import datetime

class EngagementCampaign(Base):
    __tablename__ = "engagement_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)  # Length can be adjusted
    description = Column(Text)
    status = Column(String(50), default="active")  # Default status can be "active"
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, Text, DateTime
from ..dependencies.database import Base
from datetime import datetime

class CustomerSupport(Base):
    __tablename__ = "customer_support"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)  # Add a length for the VARCHAR type
    description = Column(Text)
    status = Column(String(50), default="open")  # Optionally add a length for the status
    created_at = Column(DateTime, default=datetime.utcnow)

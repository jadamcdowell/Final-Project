from sqlalchemy.orm import Session
from ..models.engagement_campaign import EngagementCampaign
from ..schemas.engagement_campaign import EngagementCampaignCreate

# Function to create a new engagement campaign
def create_campaign(db: Session, request: EngagementCampaignCreate):
    campaign = EngagementCampaign(**request.dict())  # Create a new campaign from request data
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

# Function to get all engagement campaigns
def read_all_campaigns(db: Session):
    return db.query(EngagementCampaign).all()

# Function to get a specific campaign by ID
def read_campaign(db: Session, campaign_id: int):
    return db.query(EngagementCampaign).filter(EngagementCampaign.id == campaign_id).first()

# Function to update an engagement campaign
def update_campaign(db: Session, request: EngagementCampaignCreate, campaign_id: int):
    campaign = db.query(EngagementCampaign).filter(EngagementCampaign.id == campaign_id).first()
    if campaign:
        for key, value in request.dict().items():
            setattr(campaign, key, value)
        db.commit()
        db.refresh(campaign)
    return campaign

# Function to delete an engagement campaign
def delete_campaign(db: Session, campaign_id: int):
    campaign = db.query(EngagementCampaign).filter(EngagementCampaign.id == campaign_id).first()
    if campaign:
        db.delete(campaign)
        db.commit()
        return {"message": "Campaign deleted successfully"}
    return {"message": "Campaign not found"}

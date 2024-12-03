from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import engagement_campaign as controller
from ..schemas import engagement_campaign as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Engagement Campaign'],
    prefix="/engagement-campaigns"
)

# Endpoint to create a new engagement campaign
@router.post("/", response_model=schema.EngagementCampaignOut)
def create_campaign(request: schema.EngagementCampaignCreate, db: Session = Depends(get_db)):
    return controller.create_campaign(db=db, request=request)

# Endpoint to get all engagement campaigns
@router.get("/", response_model=list[schema.EngagementCampaignOut])
def read_all_campaigns(db: Session = Depends(get_db)):
    return controller.read_all_campaigns(db)

# Endpoint to get a specific engagement campaign by its ID
@router.get("/{campaign_id}", response_model=schema.EngagementCampaignOut)
def read_campaign(campaign_id: int, db: Session = Depends(get_db)):
    return controller.read_campaign(db, campaign_id=campaign_id)

# Endpoint to update a specific engagement campaign
@router.put("/{campaign_id}", response_model=schema.EngagementCampaignOut)
def update_campaign(campaign_id: int, request: schema.EngagementCampaignCreate, db: Session = Depends(get_db)):
    return controller.update_campaign(db=db, request=request, campaign_id=campaign_id)

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    return controller.delete_campaign(db=db, campaign_id=campaign_id)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..controllers import engagement_campaign as controller
from ..schemas import engagement_campaign as schema
from ..dependencies.database import get_db
from ..models.restaurant_staff import RestaurantStaff  # Assuming this is your model for staff roles

router = APIRouter(
    tags=['Engagement Campaign'],
    prefix="/engagement-campaigns"
)

# Helper function to check if the staff member is a manager
def is_manager(db: Session, staff_id: int):
    """
    Verify if the given staff ID belongs to a manager.
    Raises an HTTPException if not.
    """
    staff = db.query(RestaurantStaff).filter(RestaurantStaff.staff_id == staff_id).first()
    if not staff or staff.role.lower() != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. Only managers can perform this action."
        )

# Endpoint to create a new engagement campaign
@router.post("/", response_model=schema.EngagementCampaignOut)
def create_campaign(request: schema.EngagementCampaignCreate, staff_id: int, db: Session = Depends(get_db)):
    """
    Create a new engagement campaign. Only managers can perform this action.
    """
    is_manager(db, staff_id)  # Check if the user is a manager
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
def update_campaign(campaign_id: int, request: schema.EngagementCampaignCreate, staff_id: int, db: Session = Depends(get_db)):
    """
    Update an engagement campaign. Only managers can perform this action.
    """
    is_manager(db, staff_id)  # Check if the user is a manager
    return controller.update_campaign(db=db, request=request, campaign_id=campaign_id)

# Endpoint to delete a specific engagement campaign
@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, staff_id: int, db: Session = Depends(get_db)):
    """
    Delete an engagement campaign. Only managers can perform this action.
    """
    is_manager(db, staff_id)  # Check if the user is a manager
    return controller.delete_campaign(db=db, campaign_id=campaign_id)

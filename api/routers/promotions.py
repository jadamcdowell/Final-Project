from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..controllers import promotions as promo_controller  # Import promotion controller functions
from ..schemas import promotions as promo_schema  # Import updated promotion schemas
from ..models import restaurant_staff as staff_model  # Import the staff model
from ..dependencies.database import get_db  # Database dependency

# Create an APIRouter instance for the "Promotions" route
router = APIRouter(
    tags=["Promotions"],
    prefix="/promotions"
)

# Endpoint to get all promotions
@router.get("/", response_model=list[promo_schema.PromotionOut])
def read_all_promotions(db: Session = Depends(get_db)):
    # Calls the controller to fetch all promotions from the database
    return promo_controller.read_all(db)


# Endpoint to create a new promotion (Only Managers can create promotions)
@router.post("/", response_model=promo_schema.PromotionOut)
def create_promotion(
    request: promo_schema.PromotionCreate,
    staff_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """
        Create a promotion. Only managers can perform this action.
    """
    # Check if the staff is a Manager
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff member not found.")
    if staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Only Managers can create promotions.")

    # Calls the controller to create a new promotion
    return promo_controller.create_promotion(db=db, request=request, staff_id=staff_id)


# Endpoint to get a specific promotion by ID
@router.get("/{promo_id}", response_model=promo_schema.PromotionOut)
def read_one_promotion(promo_id: int, db: Session = Depends(get_db)):
    # Calls the controller to fetch a specific promotion by ID
    return promo_controller.read_one(db, promo_id=promo_id)


# Endpoint to update an existing promotion (Only Managers can update promotions)
@router.put("/{promo_id}", response_model=promo_schema.PromotionOut)
def update_promotion(promo_id: int, request: promo_schema.PromotionCreate, staff_id: int,
                     db: Session = Depends(get_db)):
    """
        Update a promotion. Only managers can perform this action.
    """
    # Check if the staff is a Manager
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff member not found.")
    if staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Only Managers can update promotions.")

    # Calls the controller to update the promotion
    return promo_controller.update_promotion(db=db, promo_id=promo_id, request=request, staff_id=staff_id)


# Endpoint to delete a promotion (Only Managers can delete promotions)
@router.delete("/{promo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(promo_id: int, staff_id: int, db: Session = Depends(get_db)):
    """
        Delete a promotion. Only managers can perform this action.
    """
    # Check if the staff is a Manager
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff member not found.")
    if staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only Managers can delete promotions.")

    # Calls the controller to delete the promotion, passing staff_id as well
    promo_controller.delete_promotion(db=db, promo_id=promo_id, staff_id=staff_id)

    return {"message": "Promotion deleted successfully."}
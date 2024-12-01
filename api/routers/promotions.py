from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..controllers import promotions as controller  # Import the promotions controller functions
from ..schemas import promotions as schema  # Import the promotions schemas
from ..schemas.promotions import PromotionCreate, PromotionOut  # Import specific schema models
from ..models.promotions import Promotion  # Import the Promotion model
from ..dependencies.database import get_db  # Import the database dependency to get DB session

# Create an APIRouter instance for the "Promotions" route
router = APIRouter(
    tags=['Promotions'],
    prefix="/promotions"
)


# Endpoint to create a new promotion
@router.post("/", response_model=PromotionOut)
def create_promotion(promotion: PromotionCreate, db: Session = Depends(get_db)):
    # Creates a new promotion in the database using the request data
    db_promotion = Promotion(
        order_id=promotion.order_id,
        user_id=promotion.user_id,
        is_valid=promotion.is_valid
    )
    db.add(db_promotion)  # Add the new promotion to the session
    db.commit()  # Commit the transaction
    db.refresh(db_promotion)  # Refresh the instance with the new data
    return db_promotion  # Return the newly created promotion


# Endpoint to get all promotions
@router.get("/", response_model=list[schema.PromotionOut])
def read_all(db: Session = Depends(get_db)):
    # Fetches all promotions from the database
    return controller.read_all(db)


# Endpoint to get a specific promotion by ID
@router.get("/{promotion_id}", response_model=schema.PromotionOut)
def read_one(promotion_id: int, db: Session = Depends(get_db)):
    # Fetches a specific promotion by its ID
    return controller.read_one(db, promotion_id=promotion_id)


# Endpoint to update a promotion by ID
@router.put("/{promotion_id}", response_model=schema.PromotionOut)
def update(promotion_id: int, request: schema.PromotionCreate, db: Session = Depends(get_db)):
    # Updates a specific promotion by its ID and returns the updated promotion
    return controller.update_promotion(db=db, promotion_id=promotion_id, promotion=request)


# Endpoint to delete a promotion by ID
@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(promotion_id: int, db: Session = Depends(get_db)):
    # Fetches the promotion by ID to check if it exists
    db_promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if db_promotion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Promotion with ID {promotion_id} not found"
        )
    # Delete the promotion
    db.delete(db_promotion)
    db.commit()
    return {"detail": f"Promotion with ID {promotion_id} deleted successfully"}
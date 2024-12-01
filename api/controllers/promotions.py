from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import promotions as model  # Import the Promotion model
from ..schemas import promotions as schema  # Import the Promotion schema


# Create a new promotion
def create_promotion(db: Session, promotion: schema.PromotionCreate):
    # Create a new Promotion object
    db_promotion = model.Promotion(
        is_valid=promotion.valid,  # Set promotion validity status
        order_id=promotion.order_id,
        user_id=promotion.user_id
    )

    try:
        db.add(db_promotion)  # Add the promotion to the DB session
        db.commit()  # Commit the transaction
        db.refresh(db_promotion)  # Refresh the object with DB data
    except Exception as e:
        db.rollback()  # Rollback if error occurs
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))  # Raise error

    return db_promotion


# Get all promotions
def read_all(db: Session):
    return db.query(model.Promotion).all()  # Return all promotions


# Get a single promotion by ID
def read_one(db: Session, promotion_id: int):
    db_promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
    if not db_promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")  # 404 if not found
    return db_promotion


# Update a promotion
def update_promotion(db: Session, promotion_id: int, promotion: schema.PromotionCreate):
    # Fetch the promotion to update
    db_promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()

    if db_promotion:
        db_promotion.is_valid = promotion.is_valid  # Update validity status
        db.commit()  # Commit changes to the DB
        db.refresh(db_promotion)  # Refresh with updated data
        return db_promotion  # Return updated promotion
    else:
        return None  # Return None if not found


# Delete a promotion
def delete_promotion(db: Session, promotion_id: int):
    db_promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()

    if not db_promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")  # 404 if not found

    db.delete(db_promotion)  # Delete promotion from the DB
    db.commit()  # Commit the transaction

    return {"detail": "Promotion deleted successfully"}  # Return success message


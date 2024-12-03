from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import promotions as promo_model, restaurant_staff as staff_model  # Import models
from ..schemas import promotions as promo_schema  # Import schemas


# Fetch all promotions
def read_all(db: Session):
    promotions = db.query(promo_model.Promotion).all()
    if not promotions:
        raise HTTPException(status_code=404, detail="No promotions found.")
    return promotions


# Fetch a single promotion by ID
def read_one(db: Session, promo_id: int):
    promotion = db.query(promo_model.Promotion).filter(promo_model.Promotion.id == promo_id).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found.")
    return promotion


# Create a new promotion (only accessible by managers)
def create_promotion(db: Session, request: promo_schema.PromotionCreate, staff_id: int):
    # Fetch the staff member from the database
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found.")

    # Check if the staff role is "Manager" in a case-insensitive way
    if staff.role.lower() != "manager":  # Use lowercase for comparison
        raise HTTPException(status_code=403, detail="Only Managers can create promotions.")

    # Create and save the new promotion
    new_promotion = promo_model.Promotion(
        code=request.code,
        description=request.description,
        discount_percentage=request.discount_percentage,
        start_date=request.start_date,
        expiration_date=request.expiration_date,
        is_valid=request.is_valid,
        order_id=request.order_id,  # Ensure this is a valid order ID
        user_id=request.user_id,  # Ensure this is a valid user ID
        staff_id=staff_id  # Ensure staff_id is valid
    )
    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    return new_promotion


# Update an existing promotion (only accessible by managers)
def update_promotion(db: Session, promo_id: int, request: promo_schema.PromotionCreate, staff_id: int):
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Check if staff is a Manager
    if not staff or staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied. Only managers can update promotions.")

    # Fetch the promotion to update
    promotion = db.query(promo_model.Promotion).filter(promo_model.Promotion.id == promo_id).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found.")

    # Update promotion fields
    promotion.code = request.code
    promotion.description = request.description
    promotion.discount_percentage = request.discount_percentage
    promotion.start_date = request.start_date
    promotion.expiration_date = request.expiration_date
    promotion.is_valid = request.is_valid
    promotion.order_id = request.order_id
    promotion.user_id = request.user_id

    db.commit()  # Commit changes
    db.refresh(promotion)  # Refresh and return updated promotion
    return promotion


# Delete a promotion (only accessible by managers)
def delete_promotion(db: Session, promo_id: int, staff_id: int):
    staff = db.query(staff_model.RestaurantStaff).filter(staff_model.RestaurantStaff.staff_id == staff_id).first()

    # Check if staff is a Manager
    if not staff or staff.role.lower() != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied. Only managers can delete promotions.")

    # Fetch the promotion to delete
    promotion = db.query(promo_model.Promotion).filter(promo_model.Promotion.id == promo_id).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found.")

    # Delete the promotion
    db.delete(promotion)
    db.commit()

    return {"detail": f"Promotion with code {promotion.code} deleted successfully."}
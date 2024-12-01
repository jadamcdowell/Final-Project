from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import payment as model  # Import Payment model
from ..schemas import payment as schema  # Import Payment schema


# Get all payments
def read_all(db: Session):
    try:
        payments = db.query(model.Payment).all()  # Fetch all payments
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error fetching payments")

    return payments


# Create a new payment
def create_payment(db: Session, payment: schema.PaymentCreate):
    # Create a new Payment object
    db_payment = model.Payment(
        order_id=payment.order_id,
        user_id=payment.user_id,
        payment_method=payment.payment_method
    )

    try:
        db.add(db_payment)  # Add payment to DB
        db.commit()
        db.refresh(db_payment)  # Refresh to get updated values
    except Exception as e:
        error_message = str(e)  # Capture the exact error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating payment: {error_message}")

    return db_payment


# Update payment method
def update_payment(db: Session, payment_id: int, payment: schema.PaymentCreate):
    db_payment = db.query(model.Payment).filter(model.Payment.id == payment_id).first()

    if not db_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    db_payment.payment_method = payment.payment_method  # Update payment method

    db.commit()  # Commit changes to DB
    db.refresh(db_payment)  # Refresh to get updated values
    return db_payment


# Get a specific payment by ID
def read_one(db: Session, payment_id: int):
    db_payment = db.query(model.Payment).filter(model.Payment.id == payment_id).first()

    if not db_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    return db_payment


# Delete a payment
def delete_payment(db: Session, payment_id: int):
    db_payment = db.query(model.Payment).filter(model.Payment.id == payment_id).first()

    if not db_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    db.delete(db_payment)  # Delete payment from DB
    db.commit()  # Commit transaction to persist the delete
    
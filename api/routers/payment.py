from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..controllers import payment as controller  # Import the payment controller functions
from ..schemas import payment as schema  # Import the payment schemas
from ..dependencies.database import get_db  # Import the database dependency for DB sessions

# Create a new APIRouter instance for the "Payments" route
router = APIRouter(
    tags=['Payments'],  # Tag to group endpoints related to payments
    prefix="/payments"  # URL prefix for payments endpoints
)


# Endpoint to create a new payment
@router.post("/", response_model=schema.PaymentOut)
def create(request: schema.PaymentCreate, db: Session = Depends(get_db)):
    # Calls the controller to create a new payment in the database
    return controller.create_payment(db=db, payment=request)


# Endpoint to get all payments
@router.get("/", response_model=list[schema.PaymentOut])
def read_all(db: Session = Depends(get_db)):
    # Calls the controller to fetch all payments from the database
    return controller.read_all(db)


# Endpoint to get a specific payment by ID
@router.get("/{payment_id}", response_model=schema.PaymentOut)
def read_one(payment_id: int, db: Session = Depends(get_db)):
    # Calls the controller to fetch a specific payment by its ID
    return controller.read_one(db, payment_id=payment_id)


# Endpoint to update an existing payment by ID
@router.put("/{payment_id}", response_model=schema.PaymentOut)
def update_payment(payment_id: int, request: schema.PaymentCreate, db: Session = Depends(get_db)):
    # Calls the controller to update an existing payment and returns the updated payment
    return controller.update_payment(db=db, payment_id=payment_id, payment=request)


# Endpoint to delete a payment by ID
@router.delete("/{payment_id}")
def delete(payment_id: int, db: Session = Depends(get_db)):
    # Calls the controller to delete the payment by its ID and returns a success message
    return controller.delete_payment(db=db, payment_id=payment_id)
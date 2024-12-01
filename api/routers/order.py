from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..controllers import order as controller  # Import the order controller functions
from ..schemas import order as schema  # Import the order schemas
from ..models import order as model  # Import the order models
from ..dependencies.database import get_db  # Import the database dependency for DB sessions

# Create a new APIRouter instance for the "Orders" route
router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


# Endpoint to create a new order
@router.post("/", response_model=schema.OrderOut)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    # Calls the controller to create a new order in the database
    return controller.create_order(db=db, request=request)


# Endpoint to get all orders
@router.get("/", response_model=list[schema.OrderOut])
def read_all_orders(db: Session = Depends(get_db)):
    # Calls the controller to fetch all orders from the database
    return controller.read_all(db)


# Endpoint to get a specific order by ID
@router.get("/{order_id}", response_model=schema.OrderOut)
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    # Calls the controller to fetch a specific order by its ID
    return controller.read_one(db, order_id=order_id)


# Endpoint to update an existing order by ID
@router.put("/{order_id}", response_model=schema.Order)
def update_order(order_id: int, request: schema.OrderCreate, db: Session = Depends(get_db)):
    # Calls the controller to update an existing order, raises 404 if not found
    updated_order = controller.update(db, order_id, request)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order


# Endpoint to delete an order by ID
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    # Calls the controller to delete the order by its ID and returns success message
    controller.delete_order(db=db, order_id=order_id)
    return {"message": "Order deleted successfully"}
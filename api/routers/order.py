from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..controllers import order as controller  # Import the order controller functions
from ..schemas import order as schema  # Import the order schemas
from ..dependencies.database import get_db  # Import the database dependency for DB sessions

# Create a new APIRouter instance for the "Orders" route
router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)

# Endpoint to create a new order
@router.post("/", response_model=schema.OrderOut)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    try:
        # Calls the controller to create a new order in the database
        return controller.create_order(db=db, request=request)
    except HTTPException as e:
        raise e  # Re-raise HTTPException for known errors (like promo code validation)
    except Exception as e:
        # Catch general exceptions and return an internal server error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Endpoint to get all orders
@router.get("/", response_model=list[schema.OrderOut])
def read_all_orders(db: Session = Depends(get_db)):
    # Calls the controller to fetch all orders from the database
    return controller.read_all(db)

# Endpoint to get a specific order by ID
@router.get("/{order_id}", response_model=schema.OrderOut)
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = controller.read_one(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

# Endpoint to update an existing order by ID
@router.put("/{order_id}", response_model=schema.OrderOut)
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

# Endpoint to get an order by tracking number
@router.get("/tracking/{tracking_number}", response_model=schema.OrderOut)
def get_order_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    order = controller.get_order_by_tracking(db=db, tracking_number=tracking_number)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
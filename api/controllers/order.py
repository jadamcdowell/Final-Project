from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import order as model  # Import Order model
from ..schemas import order as schema  # Import Order schema

# Get all orders
def read_all(db: Session):
    try:
        orders = db.query(model.Order).all()  # Fetch all orders
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))  # Capture error details
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return orders

# Create an order with associated order items
def create_order(db: Session, request: schema.OrderCreate):
    # Create a new order with user_id, order_type (pickup or delivery), and status (defaults to "pending")
    new_order = model.Order(
        user_id=request.user_id,
        order_type=request.order_type,
        status="pending"  # Default status
    )
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Add each order item to the order
        for item in request.order_items:
            order_item = model.OrderItem(
                quantity=item.quantity,
                menu_item_id=item.menu_item_id,
                order_id=new_order.id
            )
            db.add(order_item)

        db.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))  # Capture error details
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order

# Get a single order by ID
def read_one(db: Session, order_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()  # Fetch order by ID
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return order

# Update an existing order and its items
def update(db: Session, order_id: int, request: schema.OrderCreate):
    order = db.query(model.Order).filter(model.Order.id == order_id).first()  # Fetch order by ID
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Update order fields
    order.user_id = request.user_id  # Update user_id (if necessary)
    order.order_type = request.order_type  # Update order_type (pickup or delivery)
    order.status = request.status  # Update status (e.g., 'pending', 'completed')

    # Remove existing order items and add new ones
    for item in order.order_items:
        db.delete(item)  # Delete existing order items

    for item_data in request.order_items:
        order_item = model.OrderItem(
            menu_item_id=item_data.menu_item_id,
            quantity=item_data.quantity,
            order_id=order.id  # Link order item to order
        )
        db.add(order_item)

    db.commit()  # Commit changes
    db.refresh(order)  # Refresh and return updated order
    return order

# Delete a specific order by ID
def delete_order(db: Session, order_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()  # Fetch order by ID
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Delete associated order items
        db.query(model.OrderItem).filter(model.OrderItem.order_id == order_id).delete()

        # Delete the order
        db.delete(order)

        db.commit()  # Commit transaction

    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))  # Capture error details
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

# Get an order by its tracking number
def get_order_by_tracking(db: Session, tracking_number: str):
    try:
        order = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()  # Fetch order by tracking number
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return order

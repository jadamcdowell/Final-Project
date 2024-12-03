from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.training import TrainingModel
from ..models.restaurant_staff import RestaurantStaff  # Assuming similar staff model
from ..schemas.training import TrainingCreate

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

# Create a training ticket
def create_ticket(db: Session, request: TrainingCreate, staff_id: int):
    """
    Create a new training ticket. Restricted to managers.
    """
    is_manager(db, staff_id)
    ticket = TrainingModel(**request.dict())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

# Read all training tickets
def read_all_tickets(db: Session):
    """
    Retrieve all training tickets.
    """
    return db.query(TrainingModel).all()

# Read a single training ticket by ID
def read_ticket(db: Session, ticket_id: int):
    """
    Retrieve a specific training ticket by its ID.
    """
    ticket = db.query(TrainingModel).filter(TrainingModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Ticket not found"
        )
    return ticket

# Update a training ticket
def update_ticket(db: Session, ticket_id: int, request: TrainingCreate, staff_id: int):
    """
    Update a training ticket. Restricted to managers.
    """
    is_manager(db, staff_id)
    ticket = db.query(TrainingModel).filter(TrainingModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    for key, value in request.dict().items():
        setattr(ticket, key, value)
    db.commit()
    db.refresh(ticket)
    return ticket

# Delete a training ticket
def delete_ticket(db: Session, ticket_id: int, staff_id: int):
    """
    Delete a training ticket. Restricted to managers.
    """
    is_manager(db, staff_id)
    ticket = db.query(TrainingModel).filter(TrainingModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket deleted successfully"}

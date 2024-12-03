from sqlalchemy.orm import Session
from ..models.customer_support import CustomerSupport
from ..schemas.customer_support import CustomerSupportCreate


# Function to create a customer support ticket
def create_ticket(db: Session, request: CustomerSupportCreate):
    ticket = CustomerSupport(**request.dict())  # Create a new ticket from request data
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


# Function to get all customer support tickets
def read_all_tickets(db: Session):
    return db.query(CustomerSupport).all()


# Function to get a specific ticket by ID
def read_ticket(db: Session, ticket_id: int):
    return db.query(CustomerSupport).filter(CustomerSupport.id == ticket_id).first()


# Function to update a customer support ticket
def update_ticket(db: Session, request: CustomerSupportCreate, ticket_id: int):
    ticket = db.query(CustomerSupport).filter(CustomerSupport.id == ticket_id).first()
    if ticket:
        for key, value in request.dict().items():
            setattr(ticket, key, value)
        db.commit()
        db.refresh(ticket)
    return ticket


# Function to delete a customer support ticket
def delete_ticket(db: Session, ticket_id: int):
    ticket = db.query(CustomerSupport).filter(CustomerSupport.id == ticket_id).first()
    if ticket:
        db.delete(ticket)
        db.commit()
    return {"message": "Ticket deleted successfully"}

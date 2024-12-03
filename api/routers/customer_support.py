from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import customer_support as controller  # Import the customer support controller functions
from ..schemas import customer_support as schema  # Import the customer support schema
from ..dependencies.database import get_db  # Import database dependency to get the DB session

# Create an APIRouter instance for the "Customer Support" route
router = APIRouter(
    tags=['Customer Support'],
    prefix="/customer-support"
)

# Endpoint to create a new customer support ticket
@router.post("/", response_model=schema.CustomerSupportOut)
def create_ticket(request: schema.CustomerSupportCreate, db: Session = Depends(get_db)):
    # Create a new customer support ticket and store it in the database
    return controller.create_ticket(db=db, request=request)


# Endpoint to get all customer support tickets
@router.get("/", response_model=list[schema.CustomerSupportOut])
def read_all_tickets(db: Session = Depends(get_db)):
    # Fetch all customer support tickets from the database
    return controller.read_all_tickets(db)


# Endpoint to get a specific customer support ticket by its ID
@router.get("/{ticket_id}", response_model=schema.CustomerSupportOut)
def read_one_ticket(ticket_id: int, db: Session = Depends(get_db)):
    # Fetch a specific customer support ticket by its ID from the database
    return controller.read_ticket(db, ticket_id=ticket_id)


# Endpoint to update a specific customer support ticket by its ID
@router.put("/{ticket_id}", response_model=schema.CustomerSupportOut)
def update_ticket(ticket_id: int, request: schema.CustomerSupportCreate, db: Session = Depends(get_db)):
    # Update an existing customer support ticket by its ticket_id
    return controller.update(db=db, request=request, ticket_id=ticket_id)


# Endpoint to delete a customer support ticket by its ID
@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    # Delete a customer support ticket from the database by its ticket_id
    return controller.delete(db=db, ticket_id=ticket_id)

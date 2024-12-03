from fastapi import APIRouter, Depends
from ..controllers import training as controller
from ..schemas import training as schema
from ..dependencies.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Training"], prefix="/training")

@router.post("/", response_model=schema.TrainingOut)
def create_ticket(request: schema.TrainingCreate, db: Session = Depends(get_db)):
    """
    Create a new training ticket.
    
    Fill out the ticket information:
    - Title: Enter a concise title of the training.
    - Description: Provide a detailed description of the training process.
    - Status: Choose one of the following options: 'open', 'in progress', 'running', 'completed', or 'closed'.
    """
    return controller.create_ticket(db=db, request=request)

@router.get("/", response_model=list[schema.TrainingOut])
def read_all_tickets(db: Session = Depends(get_db)):
    return controller.read_all_tickets(db)

@router.get("/{ticket_id}", response_model=schema.TrainingOut)
def read_one_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return controller.read_ticket(db=db, ticket_id=ticket_id)

@router.put("/{ticket_id}", response_model=schema.TrainingOut)
def update_ticket(ticket_id: int, request: schema.TrainingCreate, db: Session = Depends(get_db)):
    return controller.update_ticket(db=db, request=request, ticket_id=ticket_id)

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return controller.delete_ticket(db=db, ticket_id=ticket_id)

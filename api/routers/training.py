from fastapi import APIRouter, Depends, HTTPException
from ..controllers import training as controller
from ..schemas import training as schema
from ..dependencies.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Training"], prefix="/training")

@router.post("/", response_model=schema.TrainingOut)
def create_ticket(request: schema.TrainingCreate, staff_id: int, db: Session = Depends(get_db)):
    """
    Create a new training ticket. Only managers can perform this action.
    """
    return controller.create_ticket(db=db, request=request, staff_id=staff_id)

@router.get("/", response_model=list[schema.TrainingOut])
def read_all_tickets(db: Session = Depends(get_db)):
    return controller.read_all_tickets(db)

@router.get("/{ticket_id}", response_model=schema.TrainingOut)
def read_one_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return controller.read_ticket(db=db, ticket_id=ticket_id)

@router.put("/{ticket_id}", response_model=schema.TrainingOut)
def update_ticket(ticket_id: int, request: schema.TrainingCreate, staff_id: int, db: Session = Depends(get_db)):
    """
    Update a training ticket. Only managers can perform this action.
    """
    return controller.update_ticket(db=db, ticket_id=ticket_id, request=request, staff_id=staff_id)

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, staff_id: int, db: Session = Depends(get_db)):
    """
    Delete a training ticket. Only managers can perform this action.
    """
    return controller.delete_ticket(db=db, ticket_id=ticket_id, staff_id=staff_id)
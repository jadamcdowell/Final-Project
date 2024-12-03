# app/controllers/training.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.training import TrainingModel
from ..schemas.training import TrainingCreate

def create_ticket(db: Session, request: TrainingCreate):
    ticket = TrainingModel(**request.dict())  # Create ticket from request data
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def read_all_tickets(db: Session):
    return db.query(TrainingModel).all()

def read_ticket(db: Session, ticket_id: int):
    ticket = db.query(TrainingModel).filter(TrainingModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

def update_ticket(db: Session, request: TrainingCreate, ticket_id: int):
    ticket = db.query(TrainingModel).filter(TrainingModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for key, value in request.dict().items():
        setattr(ticket, key, value)
    db.commit()
    db.refresh(ticket)
    return ticket

def delete_ticket(db: Session, ticket_id: int):
    ticket = db.query(TrainingModel).filter(TrainingModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket deleted successfully"}

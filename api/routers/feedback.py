from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import feedback as controller  # Import the feedback controller
from ..schemas import feedback as schema  # Import the feedback schema
from ..dependencies.database import get_db  # Import the database dependency

# Create a new APIRouter instance for the "Feedback" route
router = APIRouter(
    tags=['Feedback'],
    prefix="/feedback"
)


# Endpoint to create new feedback
@router.post("/", response_model=schema.FeedbackOut)
def create_feedback(request: schema.FeedbackCreate, db: Session = Depends(get_db)):
    # Calls the controller to handle feedback creation
    return controller.create(db=db, request=request)


# Endpoint to get all feedback
@router.get("/", response_model=list[schema.FeedbackOut])
def read_all_feedback(db: Session = Depends(get_db)):
    # Calls the controller to fetch all feedback
    return controller.read_all(db)


# Endpoint to get a single feedback by ID
@router.get("/{feedback_id}", response_model=schema.FeedbackOut)
def read_one_feedback(feedback_id: int, db: Session = Depends(get_db)):
    # Calls the controller to fetch feedback by ID
    return controller.read_one(db, feedback_id=feedback_id)


# Endpoint to update existing feedback by ID
@router.put("/{feedback_id}", response_model=schema.FeedbackOut)
def update_feedback(feedback_id: int, request: schema.FeedbackCreate, db: Session = Depends(get_db)):
    # Calls the controller to update feedback by ID
    return controller.update(db=db, request=request, feedback_id=feedback_id)


# Endpoint to delete feedback by ID
@router.delete("/{feedback_id}")
def delete(feedback_id: int, db: Session = Depends(get_db)):
    # Calls the controller to delete feedback by ID
    return controller.delete(db=db, feedback_id=feedback_id)
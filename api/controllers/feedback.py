from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import feedback as model  # Import Feedback model
from ..schemas import feedback as schema  # Import Feedback schema


# Create new feedback
def create(db: Session, request: schema.FeedbackCreate):
    new_feedback = model.Feedback(
        comments=request.comments,
        rating=request.rating,
        user_id=request.user_id
    )
    try:
        db.add(new_feedback)  # Add and commit new feedback
        db.commit()
        db.refresh(new_feedback)  # Refresh to get the generated ID
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))

    return new_feedback


# Get all feedback
def read_all(db: Session):
    try:
        return db.query(model.Feedback).all()  # Retrieve all feedback
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


# Get feedback by ID
def read_one(db: Session, feedback_id: int):
    feedback = db.query(model.Feedback).filter(model.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return feedback


# Update feedback by ID
def update(db: Session, feedback_id: int, request):
    feedback = db.query(model.Feedback).filter(model.Feedback.id == feedback_id)
    if not feedback.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    feedback.update(request.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return feedback.first()


# Delete feedback by ID
def delete(db: Session, feedback_id: int):
    feedback = db.query(model.Feedback).filter(model.Feedback.id == feedback_id)
    if not feedback.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    feedback.delete(synchronize_session=False)
    db.commit()
    return {"message": "Feedback deleted successfully!"}
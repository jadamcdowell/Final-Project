from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import user as model  # Import the User model
from ..schemas.user import UserCreate, UserOut  # Import Pydantic schemas for creating and returning users
from api.models.user import User  # Import User model for querying


# Create a new user
def create_user(db: Session, request: UserCreate):
    # Create a new User object and map the request data to the model fields
    new_user = model.User(
        name=request.username,  # maps Pydantic `username` to SQLAlchemy `name`
        email=request.email,
        password=request.password
    )

    try:
        db.add(new_user)  # Add the new user to the session
        db.commit()  # Commit the transaction
        db.refresh(new_user)  # Refresh the user object with the committed data
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])  # Extract and raise database error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return UserOut(  # Return the user details in the response format
        id=new_user.id,
        username=new_user.name,
        name=new_user.name,
        email=new_user.email,
        created_at=new_user.created_at
    )


# Retrieve all users
def read_all(db: Session):
    try:
        users = db.query(model.User).all()  # Query all users from the database
        # Map each user to the UserOut schema
        return [UserOut(
            id=user.id,
            username=user.name,
            name=user.name,
            email=user.email,
            created_at=user.created_at
        ) for user in users]
    except SQLAlchemyError as e:
        error_message = str(e)  # Capture and raise error if query fails
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)


# Retrieve a single user by ID
def read_one(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()  # Query user by ID
    if not user:
        raise HTTPException(status_code=404, detail="User not found")  # Return error if not found

    return UserOut(  # Return user details in the specified output format
        id=user.id,
        username=user.name,
        name=user.name,
        email=user.email,
        created_at=user.created_at
    )


# Update user details
def update(db: Session, user_id: int, request):
    try:
        user = db.query(model.User).filter(model.User.id == user_id).first()  # Query user by ID

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")  # Error if not found

        # Update the user with the provided data
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()  # Commit the transaction

        return user  # Return the updated user

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))  # Handle database errors


# Delete a user by ID
def delete(db: Session, user_id: int):
    try:
        user = db.query(model.User).filter(model.User.id == user_id)  # Query user by ID
        if not user.first():  # If the user does not exist
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

        user.delete(synchronize_session=False)  # Delete the user
        db.commit()  # Commit the transaction
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])  # Capture and raise error if deletion fails
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {"message": "User deleted successfully!"}  # Return success message

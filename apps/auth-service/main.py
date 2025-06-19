import uuid

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, User
from schemas import UserCreate, Token, UserResponse
from auth import create_access_token, verify_password, pwd_context


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth-Service MVP")


@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    
    db_user = User(id=uuid.uuid4(), email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": db_user.email})

    response = {"access_token": access_token, "token_type": "bearer"}

    return JSONResponse(content=response)


@app.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})

    response = {"access_token": access_token, "token_type": "bearer"}

    return JSONResponse(content=response)


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    response = {"id": str(user.id), "email": user.email}

    return JSONResponse(content=response)


@app.get("/_all_users")
def _get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    response = [
        {
            "id": str(user.id),
            "email": user.email,
            "password_hash": user.password_hash
        }
        for user in users
    ]
    
    return JSONResponse(content=response)
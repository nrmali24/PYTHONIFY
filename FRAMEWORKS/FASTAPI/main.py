from fastapi import FastAPI, Depends, HTTPException
import string
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. Database setup (SQLAlchemy)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Define models (SQLAlchemy)
class User(Base):
    __tablename__ = 'users'
    id=Column(Integer, primary_key=True, index=True,autoincrement=True,default=any)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# 3. Pydantic schemas for validation
class UserBase(BaseModel):
    name: str
    email: str
    password: str
    id: int

    class Config:
        from_attributes = True

# 4. FastAPI app
app = FastAPI()

# 5. Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 6. CRUD operations
def create_user(db: Session, user: UserBase):
    db_user = User(id=user.id,name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

# 7. Routes (Endpoints)
@app.post("/create/users", response_model=None)
def create_user_endpoint(user: UserBase, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=None)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/allusers", response_model=None)
def get_user_endpoint(db: Session = Depends(get_db)):
    db_user = get_all_users(db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 8. Create the database tables (optional)
Base.metadata.create_all(bind=engine)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
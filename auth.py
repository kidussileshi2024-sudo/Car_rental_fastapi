import os
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models import Employee
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise RuntimeError("JWT_SECRET_KEY must be configured with at least 32 characters")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        emp_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    employee = session.scalar(select(Employee).where(Employee.Emp_id == emp_id))
    if employee is None:
        raise HTTPException(status_code=401, detail="Employee not found", headers={"WWW-Authenticate": "Bearer"})
    return {"Emp_id": employee.Emp_id, "Name": employee.Name, "Role": employee.Role}


def require_mechanic(current_user=Depends(get_current_user)):
    if current_user["Role"] != "Mechanic":
        raise HTTPException(status_code=403, detail="Mechanic access required")
    return current_user

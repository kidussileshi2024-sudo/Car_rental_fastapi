from datetime import datetime, timedelta, timezone
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import ALGORITHM, SECRET_KEY
from database import engine
from models import Employee as EmployeeModel
router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    try:
        emp_id = int(form_data.username)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    with Session(engine) as session:
        employee = session.scalar(
            select(EmployeeModel).where(
                EmployeeModel.Emp_id == emp_id
            )
        )

        if employee is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token_data = {
            "sub": str(employee.Emp_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        }

        token = jwt.encode(
            token_data,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

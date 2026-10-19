from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import get_current_user, get_session, require_mechanic
from models import Branch, Booking as BookingModel, Car, Category, Customer as CustomerModel, Inspection as InspectionModel, Maintenance, Payment
from schemas import BookingCreate, BookingResponse, CarCreate, CarListResponse, CarResponse, CarUpdate, CustomerCreate, CustomerResponse, InspectionResponse, InspectionUpdate, MaintenanceResponse, MaintenanceUpdate, PaymentResponse, PaymentUpdate
from services.rental_service import create_open_inspection
router = APIRouter()

@router.get("/customers", response_model=list[CustomerResponse])
def get_customers(session: Session = Depends(get_session), Phone_no: str | None = None)-> list[CustomerResponse]:
        if Phone_no is not None:
            customer = session.scalar(
                select(CustomerModel).where(
                    CustomerModel.Phone_no == Phone_no
                )
            )

            if customer is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Customer with phone number {Phone_no} not found"
                )

            return [customer]
        
        return session.scalars(select(CustomerModel)).all()

@router.post("/customer")
def add_customer(customer: CustomerCreate, session: Session = Depends(get_session)):
        new_customer = CustomerModel(
            Name=customer.Name,
            Address=customer.Address,
            License_num=customer.License_num,
            Age=customer.Age,
            Phone_no=customer.Phone_no
        )

        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)

        return new_customer

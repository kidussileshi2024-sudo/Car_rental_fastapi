from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import get_current_user, get_session, require_mechanic
from models import Branch, Booking as BookingModel, Car, Category, Customer as CustomerModel, Inspection as InspectionModel, Maintenance, Payment
from schemas import BookingCreate, BookingResponse, CarCreate, CarListResponse, CarResponse, CarUpdate, CustomerCreate, CustomerResponse, InspectionResponse, InspectionUpdate, MaintenanceResponse, MaintenanceUpdate, PaymentResponse, PaymentUpdate
from services.rental_service import create_open_inspection
router = APIRouter()

@router.get("/inspections/open", response_model=list[InspectionResponse])
def get_open_inspections(
    session: Session = Depends(get_session),
    current_user = Depends(require_mechanic)
):
        inspections = session.scalars(
            select(InspectionModel).where(
                InspectionModel.Inspection_done == False
            )
        ).all()

        return inspections

@router.patch("/inspections/{inspection_id}")
def complete_inspection(
    inspection_id: int,
    inspection: InspectionUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(require_mechanic)
):      
        booking_emp = session.scalar(
            select(BookingModel.Emp_id).where(
                BookingModel.B_id == InspectionModel.Book_id
            )
        )

        existing_inspection = session.scalar(
            select(InspectionModel).where(
                InspectionModel.I_id == inspection_id
            )
        )

        if existing_inspection is None:
            raise HTTPException(
                status_code=404,
                detail="Inspection not found"
            )

        if existing_inspection.Inspection_done:
            raise HTTPException(
                status_code=400,
                detail="Inspection already completed"
            )
        car = session.scalar(
        select(Car).where(
        Car.C_id == existing_inspection.Car_id
        )
        )

        if car is None:
            raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

        existing_inspection.Em_id = inspection.Em_id
        existing_inspection.Damages = inspection.Damages
        existing_inspection.Fine = inspection.Fine
        if inspection.Fine is not None and inspection.Fine > 0:
            existing_inspection.Inspection_done = True
            new_payment = Payment(
                B_id=existing_inspection.Book_id,
                Method=None,
                Amount=inspection.Fine,
                Type="Fine",
                Emp_id=booking_emp,
                Invoice=None
            )
            session.add(new_payment)
            new_maintenance = Maintenance(
            Car_id=existing_inspection.Car_id,
            Description=existing_inspection.Damages,
            Start_date=date.today(),
            End_date=None,
        )
            session.add(new_maintenance)
        else:
            existing_inspection.Inspection_done = True
            car.IS_available = True

        session.commit()
        session.refresh(existing_inspection)

        return existing_inspection

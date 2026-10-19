from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import get_current_user, get_session, require_mechanic
from models import Branch, Booking as BookingModel, Car, Category, Customer as CustomerModel, Inspection as InspectionModel, Maintenance, Payment
from schemas import BookingCreate, BookingResponse, CarCreate, CarListResponse, CarResponse, CarUpdate, CustomerCreate, CustomerResponse, InspectionResponse, InspectionUpdate, MaintenanceResponse, MaintenanceUpdate, PaymentResponse, PaymentUpdate
from services.rental_service import create_open_inspection
router = APIRouter()

@router.post("/bookings")
def create_booking(booking: BookingCreate, session: Session = Depends(get_session)):

        customer = session.scalar(
            select(CustomerModel).where(
                CustomerModel.C_id == booking.Cu_id
            )
        )

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        car = session.scalar(
            select(Car).where(
                Car.C_id == booking.Car_id
            )
        )

        if car is None:
            raise HTTPException(
                status_code=404,
                detail="Car not found"
            )

        if not car.IS_available:
            raise HTTPException(
                status_code=400,
                detail="Car is not available"
            )

        new_booking = BookingModel(
            Cu_id=booking.Cu_id,
            Car_id=booking.Car_id,
            Start_date=booking.Start_date,
            End_date= None,
            Emp_id=booking.Emp_id
        )

        car.IS_available = False

        session.add(new_booking)
        session.commit()
        session.refresh(new_booking)

        return new_booking

@router.get("/bookings/{booking_id}")
def get_booking(booking_id: int, session: Session = Depends(get_session)):
        booking = session.scalar(
            select(BookingModel).where(
                BookingModel.B_id == booking_id
            )
        )

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return booking

@router.get("/bookings", response_model=list[BookingResponse])
def get_bookings(
    customer_id: int | None = None,
    branch_id: int | None = None,
    car_id: int | None = None,
    available: bool | None = None,
    session: Session = Depends(get_session),
):
    # 1. Validate customer ID
    if customer_id is not None:
        customer = session.scalar(
            select(CustomerModel).where(
                CustomerModel.C_id == customer_id
            )
        )

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail=f"Customer with ID {customer_id} not found",
            )

    # 2. Validate branch ID
    if branch_id is not None:
        branch = session.scalar(
            select(Branch).where(
                Branch.B_id == branch_id
            )
        )

        if branch is None:
            raise HTTPException(
                status_code=404,
                detail=f"Branch with ID {branch_id} not found",
            )

    # 3. Validate car ID
    if car_id is not None:
        car = session.scalar(
            select(Car).where(
                Car.C_id == car_id
            )
        )

        if car is None:
            raise HTTPException(
                status_code=404,
                detail=f"Car with ID {car_id} not found",
            )

    # 4. Build the query
    statement = (
        select(BookingModel, CustomerModel.Name)
        .join(
            CustomerModel,
            BookingModel.Cu_id == CustomerModel.C_id
        )
        .join(
            Car,
            BookingModel.Car_id == Car.C_id
        )
    )

    # 5. Apply optional filters
    if customer_id is not None:
        statement = statement.where(
            BookingModel.Cu_id == customer_id
        )

    if car_id is not None:
        statement = statement.where(
            BookingModel.Car_id == car_id
        )

    if branch_id is not None:
        statement = statement.where(
            Car.Branch_id == branch_id
        )

    if available is not None:
        statement = statement.where(
            Car.IS_available == available
        )

    # 6. Execute the query
    results = session.execute(statement).all()

    # 7. Format the response
    return [
        {
            "B_id": booking.B_id,
            "Cu_id": booking.Cu_id,
            "Car_id": booking.Car_id,
            "Start_date": booking.Start_date,
            "End_date": booking.End_date,
            "Emp_id": booking.Emp_id,
            "customer_name": customer_name,
        }
        for booking, customer_name in results
    ]

@router.patch("/bookings/{booking_id}/return")
def return_car(booking_id: int, session: Session = Depends(get_session)):
        booking = session.scalar(
            select(BookingModel).where(
                BookingModel.B_id == booking_id
            )
        )

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if booking.End_date is not None:
            raise HTTPException(
                status_code=400,
                detail="Car has already been returned"
            )

        car = session.scalar(
            select(Car).where(
                Car.C_id == booking.Car_id
            )
        )

        if car is None:
            raise HTTPException(
                status_code=404,
                detail="Car not found"
            )

        booking.End_date = date.today()

        # Keep car unavailable until inspection is finished
        car.IS_available = False

        inspection = create_open_inspection(session, booking)
        return_date = date.today()
        rental_days = (return_date - booking.Start_date).days

        if rental_days < 1:
             rental_days = 1
        new_payment = Payment(
            B_id=booking.B_id,
            Method=None,
            Amount=car.Price_adjs * rental_days,
            Type="Booking",
            Emp_id=booking.Emp_id,
            Invoice=None
        )

        session.add(new_payment)

        session.commit()
        session.refresh(booking)
        session.refresh(inspection)

        return {
            "message": "Car returned and inspection opened",
            "booking_id": booking.B_id,
            "inspection_id": inspection.I_id
        }

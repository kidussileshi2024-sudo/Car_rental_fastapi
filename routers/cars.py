from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import get_current_user, get_session, require_mechanic
from models import Branch, Booking as BookingModel, Car, Category, Customer as CustomerModel, Inspection as InspectionModel, Maintenance, Payment
from schemas import BookingCreate, BookingResponse, CarCreate, CarListResponse, CarResponse, CarUpdate, CustomerCreate, CustomerResponse, InspectionResponse, InspectionUpdate, MaintenanceResponse, MaintenanceUpdate, PaymentResponse, PaymentUpdate
from services.rental_service import create_open_inspection
router = APIRouter()

@router.get("/cars")

def get_cars(

    available: bool | None = None,

    branch_id: int | None = None,

    category_id: int | None = None,

    session: Session = Depends(get_session),

)-> list[CarListResponse]:

    statement = select(Car)

    if available is not None:

        statement = statement.where(

            Car.IS_available == available

        )

    if branch_id is not None:
        branch = session.scalar(
        select(Branch).where(Branch.B_id == branch_id)
    )
        if branch is None:
            raise HTTPException(
            status_code=404,
            detail=f"Branch with ID {branch_id} not found"
        )

    if category_id is not None:
        category = session.scalar(
        select(Category).where(Category.C_id == category_id)
    )
        if category is None:
            raise HTTPException(
            status_code=404,
            detail=f"Category with ID {category_id} not found"
        )

    return session.scalars(statement).all()

@router.get("/cars/{car_id}", response_model=CarResponse)
def get_car(
    car_id: int,
    session: Session = Depends(get_session)
):
    car = session.scalar(
        select(Car).where(Car.C_id == car_id)
    )

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car

@router.post("/cars")
def add_car(
    car: CarCreate,
    session: Session = Depends(get_session)
):
    new_car = Car(
        Plate_no=car.Plate_no,
        Price_adjs=car.Price_adjs,
        Model_id=car.Model_id,
        Branch_id=car.Branch_id,
        Color=car.Color,
        IS_available=car.IS_available
    )

    session.add(new_car)
    session.commit()
    session.refresh(new_car)

    return new_car

@router.patch("/cars/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car: CarUpdate, session: Session = Depends(get_session)):
        existing_car = session.scalar(
            select(Car).where(Car.C_id == car_id)
        )

        if existing_car is None:
            raise HTTPException(status_code=404, detail="Car not found")

        update_data = car.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_car, field, value)

        session.commit()
        session.refresh(existing_car)

        return existing_car

@router.delete("/cars/{car_id}")
def delete_car(car_id: int, session: Session = Depends(get_session)):
        car = session.scalar(
            select(Car).where(Car.C_id == car_id)
        )

        if car is None:
            raise HTTPException(status_code=404, detail="Car not found")

        session.delete(car)
        session.commit()

        return {"message": "Car deleted"}

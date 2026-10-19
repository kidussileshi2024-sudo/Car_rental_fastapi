from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import get_current_user, get_session, require_mechanic
from models import Branch, Booking as BookingModel, Car, Category, Customer as CustomerModel, Inspection as InspectionModel, Maintenance, Payment
from schemas import BookingCreate, BookingResponse, CarCreate, CarListResponse, CarResponse, CarUpdate, CustomerCreate, CustomerResponse, InspectionResponse, InspectionUpdate, MaintenanceResponse, MaintenanceUpdate, PaymentResponse, PaymentUpdate
from services.rental_service import create_open_inspection
router = APIRouter()

@router.get("/maintenance", response_model=list[MaintenanceResponse])
def get_maintenance(
    car_id: int | None = None,
    active_only: bool | None = None,
    session: Session = Depends(get_session)
):
    statement = select(Maintenance)

    if car_id is not None:
        car = session.scalar(
            select(Car).where(Car.C_id == car_id)
        )

        if car is None:
            raise HTTPException(
                status_code=404,
                detail=f"Car with ID {car_id} not found"
            )

        statement = statement.where(
            Maintenance.Car_id == car_id
        )

    if active_only is True:
        statement = statement.where(
            Maintenance.End_date.is_(None)
        )
    elif active_only is False:
        statement = statement.where(
            Maintenance.End_date.is_not(None)
        )

    return session.scalars(statement).all()

@router.patch(
    "/maintenance/{maintenance_id}",
    response_model=MaintenanceResponse
)
def update_maintenance(
    maintenance_id: int,
    maintenance_data: MaintenanceUpdate,
    session: Session = Depends(get_session)
):
    # 1. Find the maintenance record
    maintenance = session.scalar(
        select(Maintenance).where(
            Maintenance.M_id == maintenance_id
        )
    )

    if maintenance is None:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    # 2. Get only the fields provided by the client
    update_data = maintenance_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided to update"
        )

    # 3. Validate the new dates
    new_start_date = update_data.get(
        "Start_date",
        maintenance.Start_date
    )

    new_end_date = update_data.get(
        "End_date",
        maintenance.End_date
    )

    if (
        new_end_date is not None
        and new_end_date < new_start_date
    ):
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    # 4. Find the associated car
    car = session.scalar(
        select(Car).where(
            Car.C_id == maintenance.Car_id
        )
    )

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car associated with maintenance was not found"
        )

    # 5. Handle the optional car price separately
    price_adjs = update_data.pop("Price_adjs", None)

    if price_adjs is not None:
        if price_adjs < 0:
            raise HTTPException(
                status_code=400,
                detail="Car price cannot be negative"
            )

        car.Price_adjs = price_adjs

    # 6. Update the maintenance fields
    for field, value in update_data.items():
        setattr(maintenance, field, value)

    if (
        "End_date" in update_data
        and update_data["End_date"] is not None
    ):
        other_active_maintenance = session.scalar(
            select(Maintenance).where(
                Maintenance.Car_id == maintenance.Car_id,
                Maintenance.M_id != maintenance.M_id,
                Maintenance.End_date.is_(None)
            )
        )

        if other_active_maintenance is None:
            car.IS_available = True

    try:
        session.commit()
        session.refresh(maintenance)

    except Exception:
        session.rollback()
        raise

    return maintenance

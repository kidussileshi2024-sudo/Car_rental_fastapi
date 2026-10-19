from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import get_current_user, get_session, require_mechanic
from models import Branch, Booking as BookingModel, Car, Category, Customer as CustomerModel, Inspection as InspectionModel, Maintenance, Payment
from schemas import BookingCreate, BookingResponse, CarCreate, CarListResponse, CarResponse, CarUpdate, CustomerCreate, CustomerResponse, InspectionResponse, InspectionUpdate, MaintenanceResponse, MaintenanceUpdate, PaymentResponse, PaymentUpdate
from services.rental_service import create_open_inspection
router = APIRouter()

@router.get("/payments", response_model=list[PaymentResponse])
def get_payments(
        session: Session = Depends(get_session),
        booking_id: int | None = None,
    ):
        if booking_id is not None:
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

            payments = session.scalars(
                select(Payment).where(
                    Payment.B_id == booking_id
                )
            ).all()

            return payments
        payments = session.scalars(
            select(Payment)
        ).all()

        return payments

@router.patch("/payments/{payment_id}")
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    session: Session = Depends(get_session)
):
    payment = session.scalar(
        select(Payment).where(Payment.P_id == payment_id)
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    update_data = payment_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided to update"
        )

    for field, value in update_data.items():
        setattr(payment, field, value)

    session.commit()
    session.refresh(payment)

    return payment

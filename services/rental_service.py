from datetime import date
from sqlalchemy.orm import Session
from models import Booking, Inspection


def create_open_inspection(session: Session, booking: Booking) -> Inspection:
    inspection = Inspection(
        Car_id=booking.Car_id, Em_id=None, Book_id=booking.B_id,
        date=date.today(), Damages=None, Fine=None, Inspection_done=False,
    )
    session.add(inspection)
    return inspection

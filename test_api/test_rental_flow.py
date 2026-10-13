from datetime import date, timedelta
from uuid import uuid4
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from main import app
from database import engine
from models import (
    Car,
    Customer,
    Booking,
    Employee,
    Inspection,
    Payment,
    Maintenance,
)

client = TestClient(app)


def test_complete_rental_damage_maintenance_flow():
    """
    Test:
    create customer -> book car -> return car -> damage inspection
    -> maintenance -> complete maintenance -> car available.
    """

    # --------------------------------------------------
    # 1. Find an available car and required employees
    # --------------------------------------------------
    with Session(engine) as session:
        car = session.scalar(
            select(Car)
            .where(Car.IS_available.is_(True))
            .limit(1)
        )

        employee = session.scalar(select(Employee).limit(1))

        mechanic = session.scalar(
            select(Employee)
            .where(Employee.Role == "Mechanic")
            .limit(1)
        )

        if car is None:
            pytest.skip("No available car exists")

        if employee is None:
            pytest.fail("No employee exists for booking")

        if mechanic is None:
            pytest.fail("No employee with role 'Mechanic' exists")

        car_id = car.C_id
        employee_id = employee.Emp_id
        mechanic_id = mechanic.Emp_id

    # --------------------------------------------------
    # 2. Create a customer
    # --------------------------------------------------
    unique_suffix = uuid4().hex[:4]

    customer_data = {
    "Name": "Automated Damage Test",
    "Address": "Automated Test Address",
    "License_num": f"TEST-LIC-{unique_suffix}",
    "Age": 30,
    "Phone_no": f"TEST-{unique_suffix}",
}

    customer_response = client.post(
        "/customer",
        json=customer_data,
    )

    assert customer_response.status_code in (200, 201), (
        f"Customer creation failed: {customer_response.text}"
    )

    customer_id = customer_response.json()["C_id"]

    # --------------------------------------------------
    # 3. Create a booking
    # --------------------------------------------------
    booking_data = {
        "Cu_id": customer_id,
        "Car_id": car_id,
        "Start_date": date.today().isoformat(),
        "Emp_id": employee_id,
    }

    booking_response = client.post(
        "/bookings",
        json=booking_data,
    )

    assert booking_response.status_code in (200, 201), (
        f"Booking creation failed: {booking_response.text}"
    )

    booking_id = booking_response.json()["B_id"]

    # Verify car is unavailable after booking.
    with Session(engine) as session:
        car = session.get(Car, car_id)
        assert car is not None
        assert car.IS_available is False

    # --------------------------------------------------
    # 4. Return the car
    # --------------------------------------------------
    return_response = client.patch(
        f"/bookings/{booking_id}/return"
    )

    assert return_response.status_code == 200, (
        f"Car return failed: {return_response.text}"
    )

    return_data = return_response.json()
    inspection_id = return_data["inspection_id"]

    # Verify the inspection was created and is open.
    with Session(engine) as session:
        inspection = session.get(Inspection, inspection_id)

        assert inspection is not None
        assert inspection.Inspection_done is False
        assert inspection.Book_id == booking_id

        booking_payment = session.scalar(
            select(Payment).where(
                Payment.B_id == booking_id,
                Payment.Type == "Booking",
            )
        )

        assert booking_payment is not None

        car = session.get(Car, car_id)
        assert car is not None
        assert car.IS_available is False

    # --------------------------------------------------
    # 5. Log in as a mechanic
    # --------------------------------------------------
    login_response = client.post(
        "/login",
        data={
            "username": str(mechanic_id),
            "password": "1234",
        },
    )

    assert login_response.status_code == 200, (
        f"Mechanic login failed: {login_response.text}"
    )

    token = login_response.json()["access_token"]

    mechanic_headers = {
        "Authorization": f"Bearer {token}",
    }

    # --------------------------------------------------
    # 6. Complete inspection with damage and a fine
    # --------------------------------------------------
    fine_amount = 250.00
    damage_description = "Automated test: damaged bumper"

    inspection_response = client.patch(
        f"/inspections/{inspection_id}",
        headers=mechanic_headers,
        json={
            "Em_id": mechanic_id,
            "Damages": damage_description,
            "Fine": fine_amount,
        },
    )

    assert inspection_response.status_code == 200, (
        f"Inspection failed: {inspection_response.text}"
    )

    # --------------------------------------------------
    # 7. Verify fine, maintenance, and unavailable car
    # --------------------------------------------------
    with Session(engine) as session:
        inspection = session.get(Inspection, inspection_id)

        assert inspection is not None
        assert inspection.Inspection_done is True
        assert inspection.Damages == damage_description
        assert float(inspection.Fine) == fine_amount

        fine_payment = session.scalar(
            select(Payment).where(
                Payment.B_id == booking_id,
                Payment.Type == "Fine",
            )
        )

        assert fine_payment is not None
        assert float(fine_payment.Amount) == fine_amount

        maintenance = session.scalar(
            select(Maintenance).where(
                Maintenance.Car_id == car_id,
                Maintenance.End_date.is_(None),
                Maintenance.Description == damage_description,
            )
        )

        assert maintenance is not None

        maintenance_id = maintenance.M_id

        car = session.get(Car, car_id)
        assert car is not None
        assert car.IS_available is False

    # --------------------------------------------------
    # 8. Complete maintenance
    # --------------------------------------------------
    maintenance_response = client.patch(
        f"/maintenance/{maintenance_id}",
        json={
            "End_date": date.today().isoformat(),
        },
    )

    assert maintenance_response.status_code == 200, (
        f"Maintenance completion failed: "
        f"{maintenance_response.text}"
    )

    # --------------------------------------------------
    # 9. Verify maintenance is complete and car is available
    # --------------------------------------------------
    with Session(engine) as session:
        maintenance = session.get(Maintenance, maintenance_id)

        assert maintenance is not None
        assert maintenance.End_date == date.today()

        car = session.get(Car, car_id)

        assert car is not None
        assert car.IS_available is True

    # --------------------------------------------------
    # 10. Verify the same booking cannot be returned twice
    # --------------------------------------------------
    second_return_response = client.patch(
        f"/bookings/{booking_id}/return"
    )

    assert second_return_response.status_code == 400
    assert (
        second_return_response.json()["detail"]
        == "Car has already been returned"
    )
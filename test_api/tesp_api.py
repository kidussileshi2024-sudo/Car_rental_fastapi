import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# --------------------------------
# 1. API documentation
# --------------------------------

def test_api_documentation():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "paths" in response.json()


# --------------------------------
# 2. GET endpoints
# --------------------------------

@pytest.mark.parametrize(
    "endpoint",
    [
        "/cars",
        "/customers",
        "/bookings",
        "/payments",
        "/maintenance",
    ],
)
def test_list_endpoints(endpoint):
    response = client.get(endpoint)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --------------------------------
# 3. Car endpoints
# --------------------------------

def test_get_nonexistent_car():
    response = client.get("/cars/2147483647")

    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"


def test_filter_available_cars():
    response = client.get(
        "/cars",
        params={"available": "true"},
    )

    assert response.status_code == 200

    for car in response.json():
        assert car["IS_available"] is True


def test_filter_unavailable_cars():
    response = client.get(
        "/cars",
        params={"available": "false"},
    )

    assert response.status_code == 200

    for car in response.json():
        assert car["IS_available"] is False


def test_delete_nonexistent_car():
    response = client.delete("/cars/2147483647")

    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"


# --------------------------------
# 4. Booking endpoints
# --------------------------------

def test_get_nonexistent_booking():
    response = client.get("/bookings/2147483647")

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_filter_bookings_by_nonexistent_customer():
    response = client.get(
        "/bookings",
        params={"customer_id": 2147483647},
    )

    assert response.status_code == 404


# --------------------------------
# 5. Payment endpoints
# --------------------------------

def test_payments_for_nonexistent_booking():
    response = client.get(
        "/payments",
        params={"booking_id": 2147483647},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


# --------------------------------
# 6. Maintenance endpoints
# --------------------------------

def test_maintenance_for_nonexistent_car():
    response = client.get(
        "/maintenance",
        params={"car_id": 2147483647},
    )

    assert response.status_code == 404


# --------------------------------
# 7. Authentication
# --------------------------------

def test_login_with_wrong_password():
    response = client.post(
        "/login",
        data={
            "username": "2147483647",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_inspections_require_authentication():
    response = client.get("/inspections/open")

    assert response.status_code == 401
def test_get_existing_car():
    response = client.get("/cars")

    assert response.status_code == 200

    cars = response.json()

    if not cars:
        pytest.skip("No cars exist in the database")

    car_id = cars[0]["C_id"]

    response = client.get(f"/cars/{car_id}")

    assert response.status_code == 200
    assert response.json()["C_id"] == car_id
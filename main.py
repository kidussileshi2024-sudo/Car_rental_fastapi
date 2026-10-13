
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time
import jwt
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import (
    Date,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel ,ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database import engine
from models import (
    Car ,
    Customer as CustomerModel,
    Booking as BookingModel,
    Inspection as InspectionModel,
    Employee as EmployeeModel,
    Model,
    Branch,
    Category,
    Payment,
    Maintenance,
    EmployeeMaintenance
    
   
)
from datetime import date
from schemas import (CarCreate, CarListResponse, CarResponse, CarUpdate, CustomerCreate, BookingCreate, BookingResponse, CustomerResponse, InspectionCreate, InspectionResponse, InspectionUpdate,
            CarListResponse, CustomerResponse, PaymentResponse, PaymentUpdate, MaintenanceUpdate, MaintenanceResponse)


def create_open_inspection(session: Session, booking: BookingModel):
    new_inspection = InspectionModel(
        Car_id=booking.Car_id,
        Em_id=None,
        Book_id=booking.B_id,
        date=date.today(),
        Damages=None,
        Fine=None,
        Inspection_done=False
    )

    session.add(new_inspection)

    return new_inspection




def get_session():
    with Session(engine) as session:
        yield session
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise RuntimeError(
        "JWT_SECRET_KEY must be configured with at least 32 characters"
    )
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        emp_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    employee = session.scalar(
        select(EmployeeModel).where(
            EmployeeModel.Emp_id == emp_id
        )
    )

    if employee is None:
        raise HTTPException(
            status_code=401,
            detail="Employee not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "Emp_id": employee.Emp_id,
        "Name": employee.Name,
        "Role": employee.Role
    }

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/login")
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

@app.middleware("http")
async def log_request_time(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    print(
        f"{request.method} {request.url.path} took {process_time:.4f} seconds"
    )

    return response


@app.get("/cars")

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
@app.get("/cars/{car_id}", response_model=CarResponse)
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
@app.post("/cars")
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

@app.patch("/cars/{car_id}", response_model=CarResponse)
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
@app.delete("/cars/{car_id}")
def delete_car(car_id: int, session: Session = Depends(get_session)):
        car = session.scalar(
            select(Car).where(Car.C_id == car_id)
        )

        if car is None:
            raise HTTPException(status_code=404, detail="Car not found")

        session.delete(car)
        session.commit()

        return {"message": "Car deleted"}
@app.get("/customers", response_model=list[CustomerResponse])
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
@app.post("/customer")
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
@app.post("/bookings")
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
@app.get("/bookings/{booking_id}")
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
@app.get("/bookings", response_model=list[BookingResponse])
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
@app.patch("/bookings/{booking_id}/return")
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
def require_mechanic(current_user = Depends(get_current_user)):
    if current_user["Role"] != "Mechanic":
        raise HTTPException(
            status_code=403,
            detail="Mechanic access required"
        )

    return current_user
@app.get("/inspections/open", response_model=list[InspectionResponse])
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





@app.patch("/inspections/{inspection_id}")
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
@app.get("/payments", response_model=list[PaymentResponse])
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
@app.patch("/payments/{payment_id}")
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
@app.get("/maintenance", response_model=list[MaintenanceResponse])
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
@app.patch(
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
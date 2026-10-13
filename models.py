from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Float, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from datetime import date


class Base(DeclarativeBase):
    pass


class Car(Base):
    __tablename__ = "Cars"

    C_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Plate_no: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    Price_adjs: Mapped[float | None] = mapped_column(Float, nullable=True)
    Model_id: Mapped[int] = mapped_column(Integer, nullable=False)
    Branch_id: Mapped[int] = mapped_column(Integer, nullable=False)
    Color: Mapped[str | None] = mapped_column(String(10), nullable=True)
    IS_available: Mapped[bool] = mapped_column(Boolean, nullable=False)
    maintenances: Mapped[list["Maintenance"]] = relationship(
    back_populates="car"
)
class Model(Base):
    __tablename__ = "Models"

    M_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Brand: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Price_per_day: Mapped[float | None] = mapped_column(Float, nullable=True)
    Fule_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    Cat_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Branch(Base):
    __tablename__ = "Branch"

    B_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    Phone_No: Mapped[str | None] = mapped_column(String(20), nullable=True)
    Address: Mapped[str | None] = mapped_column(String(255), nullable=True)
class Customer(Base):
    __tablename__ = "Customers"

    C_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    Name: Mapped[str] = mapped_column(String(50), nullable=False)
    Address: Mapped[str] = mapped_column(String(50), nullable=False)
    License_num: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    Age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Phone_no: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    bookings: Mapped[list["Booking"]] = relationship(back_populates="customer")
class Booking(Base):
    __tablename__ = "Booking"

    B_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    Cu_id: Mapped[int] = mapped_column(
    ForeignKey("Customers.C_id"),
    nullable=False)
    customer: Mapped["Customer"] = relationship(back_populates="bookings")
    Car_id: Mapped[int] = mapped_column(Integer, nullable=False)
    Start_date: Mapped[date] = mapped_column(Date, nullable=False)
    End_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    Emp_id: Mapped[int] = mapped_column(Integer, nullable=False)
    payments: Mapped[list["Payment"]] = relationship(
    back_populates="booking"
)
class Inspection(Base):
    __tablename__ = "Inspection"

    I_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Car_id: Mapped[int] = mapped_column(Integer, nullable=False)
    Em_id: Mapped[int | None] = mapped_column(Integer, nullable=True)    
    Book_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    Damages: Mapped[str | None] = mapped_column(String(300), nullable=True)
    Fine: Mapped[float | None] = mapped_column(Float, nullable=True)
    Inspection_done: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Employee(Base):
    __tablename__ = "Employees"

    Emp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[str] = mapped_column(String(30), nullable=False)
    B_id: Mapped[int] = mapped_column(Integer, nullable=False)
    Role: Mapped[str] = mapped_column(
        Enum("Manager", "Mechanic", "Receptionist"),
        nullable=False
    )
    maintenance_assignments: Mapped[list["EmployeeMaintenance"]] = relationship(
    back_populates="employee"
)
class Category(Base):
    __tablename__ = "Category"

    C_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    Name: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    Description: Mapped[str] = mapped_column(
        String(500), nullable=False
    )


class Payment(Base):

    __tablename__ = "payment"

    P_id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True,

        autoincrement=True

    )

    B_id: Mapped[int] = mapped_column(

        ForeignKey("Booking.B_id"),

        nullable=False

    )

    Method: Mapped[str | None] = mapped_column(

        String(30),

        nullable=True

    )

    Amount: Mapped[str] = mapped_column(

        String(50),

        nullable=False

    )

    Type: Mapped[str] = mapped_column(

        Enum("Booking", "Fine"),

        nullable=False

    )

    Emp_id: Mapped[int] = mapped_column(

        Integer,

        nullable=False

    )

    Invoice: Mapped[str | None] = mapped_column(

        String(50),

        nullable=True,

        unique=True

    )
    booking: Mapped["Booking"] = relationship(
    back_populates="payments"
)
class Maintenance(Base):
    __tablename__ = "Maintenance"

    M_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    Car_id: Mapped[int] = mapped_column(
        ForeignKey("Cars.C_id"),
        nullable=False
    )

    Start_date: Mapped[date] = mapped_column(Date, nullable=False)
    End_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    Description: Mapped[str | None] = mapped_column(String(300), nullable=True)

    car: Mapped["Car"] = relationship(back_populates="maintenances")
    employee_maintenances: Mapped[list["EmployeeMaintenance"]] = relationship(
    back_populates="maintenance"
)
class EmployeeMaintenance(Base):
    __tablename__ = "Employee_Maintenance"

    ID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    Emp_Id: Mapped[int] = mapped_column(
        ForeignKey("Employees.Emp_id"),
        nullable=False
    )

    Ment_id: Mapped[int] = mapped_column(
        ForeignKey("Maintenance.M_id"),
        nullable=False
    )

    maintenance: Mapped["Maintenance"] = relationship(
        back_populates="employee_maintenances"
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="maintenance_assignments")
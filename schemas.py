from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

class BookingResponse(BaseModel):
    B_id: int
    Cu_id: int
    Car_id: int
    Start_date: date
    End_date: date | None
    Emp_id: int
    customer_name: str
class CarUpdate(BaseModel):
    Plate_no: str | None = None
    Price_adjs: float | None = None

    Model_id: int | None = None
    Branch_id: int | None = None
    Color: str | None = None
    IS_available: bool | None = None
class CarCreate(BaseModel):
    Plate_no: str | None = None
    Price_adjs: float | None = None
    Model_id: int
    Branch_id: int
    Color: str | None = None
    IS_available: bool
class CarListResponse(BaseModel):
    C_id: int
    Plate_no: str | None
    Price_adjs: float | None
    Color: str | None
    IS_available: bool

    model_config = ConfigDict(from_attributes=True)

class CarResponse(BaseModel):

    C_id: int
    Plate_no: str | None
    Price_adjs: float | None
    Model_id: int
    Branch_id: int
    Color: str | None
    IS_available: bool
    model_config = ConfigDict(from_attributes=True)
class CustomerResponse(BaseModel):
    C_id: int
    Name: str
    Address: str
    License_num: str
    Age: int | None
    Phone_no: str
    model_config = ConfigDict(from_attributes=True)
class BookingCreate(BaseModel):
    Cu_id: int
    Car_id: int
    Start_date: date
    Emp_id: int
class CustomerCreate(BaseModel):
    Name: str
    Address: str
    License_num: str
    Age: int | None = None
    Phone_no: str
class InspectionResponse(BaseModel):
    I_id: int
    Car_id: int
    Em_id: int | None
    Book_id: int
    date: date
    Damages: str | None
    Fine: float | None
    Inspection_done: bool
class InspectionCreate(BaseModel):
    Car_id: int
    Em_id: int | None = None
    Book_id: int
    date: date
    Damages: str | None = None
    Fine: float | None = None
    Inspection_done: bool = False
class InspectionUpdate(BaseModel):
    Em_id: int
    Damages: str | None = None
    Fine: float | None = None
class LoginRequest(BaseModel):
    Emp_id: int
    Password: str
class PaymentResponse(BaseModel):
    P_id: int
    B_id: int
    Method: str | None
    Amount: str | None
    Type: str
    Emp_id: int
    Invoice: str | None

    model_config = ConfigDict(from_attributes=True)
class PaymentUpdate(BaseModel):

    Method: Optional[str] = None

    Amount: Optional[str] = None

    Invoice: Optional[str] = None
class MaintenanceCreate(BaseModel):

    Car_id: int

    Start_date: date

    End_date: date | None = None

    Description: str | None = None

class MaintenanceUpdate(BaseModel):
    Start_date: date | None = None
    End_date: date | None = None
    Description: str | None = None
    Price_adjs: float | None = None

class MaintenanceResponse(BaseModel):

    M_id: int
    Car_id: int
    Start_date: date
    End_date: date | None = None
    Description: str | None = None
    model_config = ConfigDict(from_attributes=True)

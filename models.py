from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List,Optional


class Employee(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: EmailStr
    department: str
    position: str
    salary: int
    startDate: str
    status: str


class EmployeeResponse(BaseModel):
    employees: List[Employee]


class EmployeeUpdate(BaseModel):
    firstName: Optional[str]=None
    lastName: Optional[str]=None
    email: Optional[EmailStr]=None
    department: Optional[str]=None
    position: Optional[str]=None
    salary: Optional[int]=None
    startDate: Optional[date]=None
    status: Optional[str]=None

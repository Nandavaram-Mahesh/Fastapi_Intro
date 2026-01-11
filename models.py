from pydantic import BaseModel,EmailStr
from datetime import date
from typing import List

class Employee(BaseModel):
    id:int
    firstName:str
    lastName: str
    email: EmailStr
    department: str
    position: str
    salary: int
    startDate: str
    status: str

class EmployeeResponse(BaseModel):
    employees:List[Employee]
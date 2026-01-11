import json
from typing import List

from fastapi import FastAPI, HTTPException

from models import Employee,EmployeeResponse
from utils import load_json

app = FastAPI()

@app.get('/employees',response_model=EmployeeResponse)
def employees():
    try:
        # with open('employee.json','r') as file:
        #     data = json.load(file)
        data = load_json()
        validated_data = EmployeeResponse.model_validate(data)
        return validated_data
    except FileNotFoundError:
        raise HTTPException(status_code=500 ,detail="employees.json not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/employees/{employee_id}')
def employee(employee_id:int):
    try:
        data = load_json()
        employees = data.get('employees',[])
        # print(data)
        for employee in employees:
            if employee.get("id") == employee_id:
                validated_data = Employee.model_validate(employee)
                return validated_data
        raise HTTPException(status_code=404 , detail=f"Employee with id {employee_id} not found")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404 , detail=f"Employee with id {employee_id} not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
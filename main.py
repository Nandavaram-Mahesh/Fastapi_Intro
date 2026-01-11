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
@app.post('/employee')
def create_employee(employee:Employee):
    try:
        # Load the employees from json
        data = load_json()
        
        employees = data['employees']
        
        # Validate the data
        employee = Employee.model_validate(employee)
        
        #Converting the pydnatic obj to dict  
        employee = employee.model_dump()
        
        # Add the new employee to the employees list 
        employees.append(employee)
        
        # Add the employees to the data dict
        data["employees"] = employees
        
        # Load it to the json file
        with open('employee.json','w') as file:
            json.dump(data, file,indent=2)
        
        return {"message": "Employee added", "id": employee.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))
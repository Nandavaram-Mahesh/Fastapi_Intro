import json
from typing import List

from fastapi import FastAPI, HTTPException

from models import Employee,EmployeeResponse,EmployeeUpdate
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

@app.put('/employees/{employee_id}')
def update_employee(employee_id:int , employee:EmployeeUpdate):
    try:
        # load the json data
        data = load_json()
        
        # extract employees
        employees = data.get("employees",[])
        
        # check if the employee exists with the give id
        for existing_employee in employees:
            if existing_employee.get("id") == employee_id:
                existing_employee.update(employee.model_dump(exclude_unset=True))
                # write the data back to file
                with open('employee.json','w') as file:
                    json.dump(data,file,indent=2)
                return {"message": "Employee updated", "employee": existing_employee.get("firstName")}
        # If employee not found
        raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
        
@app.delete('/employees/{employee_id}')
def delete_employee(employee_id:int):
    try:
        # Load the json Data
        data = load_json()
        
        employees = data.get("employees",[])
        
        for index , employee in enumerate(employees):
            if employee.get("id") == employee_id:
                deleted_employee = employees.pop(index)
                with open('employee.json','w') as file:
                    json.dump(data,file,indent=2)
                return {
                    "message": "Employee deleted successfully",
                    "employee_id": deleted_employee.get("id")
                }
        
        # More Cleaner Logic
        # updated_employees = [e for e in employees if e.get("id")!=employee_id]
        # data['employees'] = updated_employees  
        raise HTTPException(status_code=404 , detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
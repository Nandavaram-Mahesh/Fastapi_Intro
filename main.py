import json
from typing import List

from models import Employee,EmployeeResponse

from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get('/employees',response_model=EmployeeResponse)
def employees():
    try:
        with open('employee.json','r') as file:
            data = json.load(file)
            # validate using pydantice
            validated_data = EmployeeResponse.model_validate(data)
            return validated_data
    except FileNotFoundError:
        raise HTTPException(status_code=500 ,detail="employees.json not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

import json
def load_json():
    with open('employee.json','r') as file:
            data = json.load(file)
    return data
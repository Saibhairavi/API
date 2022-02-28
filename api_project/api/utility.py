import json
from .models import Employee

#This is to check if data sent by client app is valid or not (in json format)
def is_valid_data(data):
    try:
        p=json.loads(data)
        valid=True
    except ValueError:
        valid=False
    return valid

#this is to check if employee exists or not
def get_emp_by_id(id):
        try:
            # x=get_object_or_404(Employee,id)
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp=None        
        return emp

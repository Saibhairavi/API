import json
from .models import Student

def is_valid_json(data):
    try:
        p=json.loads(data)
        valid=True
    except ValueError:
        valid=False
    return valid

def get_student_by_id(id):
    try:
        s=Student.objects.get(id=id)
    except Student.DoesNotExist:
        s=None
    return s
    


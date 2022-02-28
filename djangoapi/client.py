import requests
import json
base_url='http://127.0.0.1:8000/'
end_point='api/'

def get_resource(id=None):
    data={}
    if id is not None:
        data={'id':id}
    resp=requests.get(base_url+end_point,data=json.dumps(data))
    print(resp.status_code)
    print(resp.json())
# get_resource(3)

def create_resource():
    new_student={'name': 'Bhairavi', 'rollno': 100, 'marks': 50, 'gm': 'John', 'gf': 'Shivani'}
    
    resp=requests.post(base_url+end_point,data=json.dumps(new_student))
    print(resp.status_code)
    print(resp.json())
# create_resource()

def update_resource(id): 
    update_student={
        'id':id,              
        'marks':9,
        'gm':'Virat',        
    }
    resp=requests.put(base_url+end_point,data=json.dumps(update_student))
    print(resp.status_code)
    print(resp.json())
# update_resource(5)

def delete_resource(id): 
    data={}
    if id is not None:
        data={'id':id}        
    resp=requests.delete(base_url+end_point,data=json.dumps(data))
    print(resp.status_code)
    print(resp.json())
delete_resource(4)


import requests
import json 
def json_resp():
    # r=requests.get('http://127.0.0.1:8000/api_json/')
    # r=requests.put('http://127.0.0.1:8000/api_json/')    
    # r=requests.post('http://127.0.0.1:8000/api_json/') 
    r=requests.delete('http://127.0.0.1:8000/api_json/')       
    print(r.status_code)
    print(r.json())
# json_resp()

# EmployeeDetail---get
def get_EmpDetail(id): 
    r=requests.get('http://127.0.0.1:8000/get_emp/'+str(id)+'/')  
    print(r.json())
    print(r.status_code)
# get_EmpDetail(12)

# EmployeeDetail---delete
def delete_EmpDetail(id): 
    r=requests.delete('http://127.0.0.1:8000/get_emp/'+str(id)+'/')  
    print(r.json())
    print(r.status_code)
# delete_EmpDetail(8)

# EmployeeDetail---put
def put_EmpDetail(id): 
    r=requests.put('http://127.0.0.1:8000/get_emp/'+str(id)+'/')  
    print(r.json())
    print(r.status_code)
# put_EmpDetail()

# EmployeeListDetails--get all emp
def get_EmpDetails(): 
    r=requests.get('http://127.0.0.1:8000/get_all_emp/')  
    print(r.json())
    print(r.status_code)
# get_EmpDetails()

# EmployeeListDetails--post
def post_EmpDetails():
    new_emp={
        'eno':2000,
        'ename':'XYZ',
        'esal':100000,
        'eaddr':'Addr1'
    }
    json_data=json.dumps(new_emp)    
    resp=requests.post('http://127.0.0.1:8000/get_all_emp/',data=json_data)
    print(resp.status_code)
    print(resp.json())
# post_EmpDetails()

#single endpoint for all methods
# EmployeeCRUD_cbv
def get_empdetail(id=None):
    data={}
    if id is not None:  #some id is passed
        # data={'id':id}
        data['id']=id
    r=requests.get('http://127.0.0.1:8000/api_api/',data=json.dumps(data))  #Base url must be stable 127.0.0.1:8000
    print(r.json())
    print(r.status_code)
# get_empdetail()   

def post_empdetail():
    new_data={'eno':1111,'ename':'PQR','esal':9999,'eaddr':'addr3'}
    r=requests.post('http://127.0.0.1:8000/api_api/',data=json.dumps(new_data))  #Base url must be stable 127.0.0.1:8000
    print(r.json())
    print(r.status_code)
# post_empdetail()

def put_empdetail(id=None):
    update_emp={
        'id':id,
        'esal':111112,
        'eaddr':'XXXXX'
    }
    data=json.dumps(update_emp)
    r=requests.put('http://127.0.0.1:8000/api_api/',data=data)  #Base url must be stable 127.0.0.1:8000
    print(r.json())
    print(r.status_code)
# put_empdetail(5)

def delete_empdetail(id=None):
    data={}
    if id is not None:  #some id is passed
        # data={'id':id}
        data['id']=id
    r=requests.delete('http://127.0.0.1:8000/api_api/',data=json.dumps(data))  #Base url must be stable 127.0.0.1:8000
    print(r.json())
    print(r.status_code)
delete_empdetail(7)
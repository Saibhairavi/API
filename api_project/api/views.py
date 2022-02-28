import json  #coming from python and not from django
from django.http import JsonResponse,HttpResponse #this is from django
from django.shortcuts import get_object_or_404, render
from .models import Employee
from .utility import *

#below for class-based view
from django.views.generic import View
from django.core.serializers import serialize  #django serialize module 
from .mixins import HttpResponseMixin,SerializeMixin

#below imports for disable csrf 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import EmployeeForm

#function based view--->http://127.0.0.1:8000/api/
def employee_data(request): 
    emp_data={
        'emp_no':100,
        'emp_name':'Bhairavi',
        'eaddr':'Pune'
    }
    x=json.dumps(emp_data)
    return HttpResponse(x,content_type='application/json')
    
#class based view --->View class present in Django
class json_resp(View,HttpResponseMixin):
    # HttpResponseMixin is child class of object class OnlyOnce
    # contains no instance variable but only
    def get(self,request,*args, **kwargs):
        emp_data={
        'emp_no':100,
        'emp_name':'Bhairavi',
        'eaddr':'Pune'
        }
        # return JsonResponse(emp_data) so conver python dict to json
        json_data=json.dumps(emp_data)
        return self.render_to_httpresponse(json_data)

    def post(self,request,*args,**kwargs):
        emp_data={
        'emp_no':100,
        'emp_name':'Bhairavi',
        'eaddr':'Pune',
        'METHOD':'POST  '
        }
        return JsonResponse(emp_data)

    def put(self,request,*args,**kargs):
        emp_data={
        'emp_no':100,
        'emp_name':'Bhairavi',
        'eaddr':'Pune',
        'METHOD':'PUT'
        }
        return JsonResponse(emp_data)
     
    def delete(self,request,*args,**kargs):
        emp_data={
        'emp_no':100,
        'emp_name':'Bhairavi',
        'eaddr':'Pune',
        'METHOD':'DELETE'
        }
        jdata=json.dumps(emp_data)
        return self.render_to_httpresponse(jdata)


#to get a single employee record    #get id,put id ,delete id
@method_decorator(csrf_exempt,name='dispatch')
class EmployeeDetail(View,SerializeMixin,HttpResponseMixin):    
    #for manual id
    def get1(self,requets,*args,**kwargs):
        emp=Employee.objects.get(id=1)
        emp_data={'ename':emp.ename,
                   'eno':emp.eno,
                   'esal':emp.esal,
                   'eaddr':emp.eaddr}
        jsondata=json.dumps(emp_data)        
        return HttpResponse(jsondata,content_type='application/json')

    #for dynamic id
    #this method will throw an error if emp does not exist
    def get2(self,requets,id,*args,**kwargs):
            emp=Employee.objects.get(id=id)
            emp_data={'ename':emp.ename,
                    'eno':emp.eno,
                    'esal':emp.esal,
                    'eaddr':emp.eaddr}
            jsondata=json.dumps(emp_data)
            #serialization-->empobjct-->dict-->to json data 
            return HttpResponse(jsondata,content_type='application/json')
    
    #single record
    def get(self,requets,id,*args,**kwargs):
        try:
            emp=Employee.objects.get(id=id)            
            # emp_data=serialize('json',[emp,],fields=['ename','eno'])
            #django serializer function 
            # emp need to pass in list since it is single 
        except Employee.DoesNotExist:
            json_data=json.dumps({'message':'Requested resource not available'})            
            return self.render_to_httpresp_status(json_data,status=404)
            # return HttpResponse(json_data,content_type='application/json',status=404)

        else:
            #successful status
            jsondata=self.serialize([emp,])                   
            # return HttpResponse(jsondata,content_type='application/json',status=200)
            return self.render_to_httpresp_status(jsondata)
        #no need to send status code since it is default in function
        
    def get_emp_by_id(self,id):
        try:
            # x=get_object_or_404(Employee,id)
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp=None        
        return emp

    def is_valid_data(self,data):
        try:
            p=json.loads(data)
            valid=True
        except ValueError:
            valid=False
        return valid
    
    def put(self,request,id,*args,**kwargs):
        emp=self.get_emp_by_id(id)
        if emp is None:  #no matched record
            json_data=json.dumps({'message':'No matched Record found..coudnt Update'})
            return self.render_to_httpresp_status(json_data,status=404)

        data=request.body #if sent data is valid or not 
        valid_json=self.is_valid_data(data)
        if not valid_json:
            json_data=json.dumps({'message':'Please send a valid data'})
            return self.render_to_httpresp_status(json_data,status=404)

        sentdata=json.loads(data) #if sent data is valid  
        #sendata is in dict
        #emp data is in emp obj---convert emp obj into dict to update data       

        emp_original_data={'eno':emp.eno,'ename':emp.ename,'esal':emp.esal,'eaddr':emp.eaddr}
        emp_original_data.update(sentdata)
        form=EmployeeForm(emp_original_data,instance=emp)
        #if we don't provide instance=emp it will create new record
        #  instaed of updating the existing one
        if form.is_valid():
            form.save(commit=True) #by default commit is true
            json_data=json.dumps({'message':'Record updated successfully'})
            return self.render_to_httpresp_status(json_data)
        
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_httpresp_status(json_data)
    #id based so in employeeDetailView 
    def delete(self,request,id,*args,**kwargs):        
        emp=Employee.objects.get(id=id)
        if emp is None:
            json_data=json.dumps({'message':'No matched record found.Could not delete'})
            return self.render_to_httpresp_status(json_data,status=404)
        
        #if record is present in the database or epm exists
        del_item=emp.delete()  #it provides tuple (a,b)
        # t=(1, {'api.Employee': 1})---->status,deleted_item
        status,deleted_item=del_item  
        if status == 1: #if 1 means successful
            json_data=json.dumps({'message':'Record deleted successfully'})
            return self.render_to_httpresp_status(json_data)
        
        #if not status=1
        json_data=json.dumps({'message':'Unable to delete .Please try agian'})
        return self.render_to_httpresp_status(json_data,status=404)
        
# ____________________________________________________________
#to get multiple employee records   #to get multoiple record,craete record
class EmployeeListDetails1(View):
    def get(self,requets,*args,**kwargs):
        all_emp=Employee.objects.all()
        json_data=serialize('json',all_emp,fields=('eno','ename','eaddr'))        
        # [{},{},{'fields':}]      --->syntax of queryset obtaied  
        dict_data=json.loads(json_data) #de-serialization.        
        allemp=[]
        for i in dict_data:
            allemp.append(i['fields'])                
        jsondata=json.dumps(allemp)  #object type to json str
        return HttpResponse(jsondata,content_type='application/json')

        #no use of mixins here.



@method_decorator(csrf_exempt,name='dispatch')
class EmployeeListDetails(View,SerializeMixin,HttpResponseMixin):

    def get(self,requet,*args,**kwargs):
        all_emp=Employee.objects.all()
        json_data=self.serialize(all_emp)
        return HttpResponse(json_data)
    
    def post(self,request,*args,**kwargs):
        # form is required for put and post
        # json_data=json.dumps({'message':'This is from post method'})
        data=request.body
        #to access post data in the method
        try:
            emp_data=json.loads(data)            
            #get post data and add it into employee table in db
        except ValueError:
            json_data=json.dumps({'message':'Please send a valid data'})
            return self.render_to_httpresp_status(json_data,status=404)
        else:
            #get post data and add it into employee table in db
            form=EmployeeForm(emp_data)
            if form.is_valid():
                #internally it calls clean_esal method in forms.py var validation
                form.save(commit=True)
                json_data=json.dumps({'message':'Resource created successfully'})
                return self.render_to_httpresp_status(json_data)

            if form.errors:
                json_data=json.dumps(form.errors)
                return self.render_to_httpresp_status(json_data,status=404)

# _______________________________________________________________________

# endpoint with url:'http://127.0.0.1:8000/api_api/' we can get single or multiple records 

# best practice## This is for single endpoint practice
@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCRUD_cbv(View,HttpResponseMixin,SerializeMixin):
    def get(self,request,*args,**kwargs):
        data=request.body  # got data from client /partener app
        valid_json=is_valid_data(data) #to checck if data is json or not  

        if not valid_json:  #if not json data
            json_data=json.dumps({'message':'Not valid data'})
            return self.render_to_httpresp_status(json_data,status=404)

        p_data=json.loads(data)   #if valid data convert into python dict        
        id=p_data.get('id',None) #to check if key 'id' is there in p_data otherwise id=None

        if id is not None:
            emp=get_emp_by_id(id)  #to check if id with employee exists or not
            if emp is None:
                json_data=json.dumps({'message':'Record Not available'})
                return self.render_to_httpresp_status(json_data,status=404)
                
            #if emp is there in db 
            json_data=self.serialize([emp,])  #convert emp obj into json data by mixin func
            return self.render_to_httpresp_status(json_data)
        
        #if id is None means get all the records convert it into son and send back to client app
        emp_data=Employee.objects.all()
        json_data=self.serialize(emp_data)
        return self.render_to_httpresp_status(json_data)

    def post(self,request,*args,**kwargs):
        data=request.body  #take the data from request
        valid_json=is_valid_data(data) #check valid data
        if not valid_json:
            json_data=json.dumps({'message':'Please send Valid Data'})
            return self.render_to_httpresp_status(json_data,status=404)
        newemp_data=json.loads(data) #if data is valid

        form=EmployeeForm(newemp_data) #create a form object to add in db
        if form.is_valid():   #implemented validations
            form.save(commit=True)
            json_data=json.dumps({'message':'Resource created successfully'})
            return self.render_to_httpresp_status(json_data)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_httpresp_status(json_data,status=404)

    def put(self,request,*args,**kwargs):
        data=request.body #get the request data
        valid_json=is_valid_data(data) #data is in json format or not
        if not valid_json:  #if not json data
            json_data=json.dumps({'message':'Not valid data'})
            return self.render_to_httpresp_status(json_data,status=404)

        p_data=json.loads(data)   #if valid data convert into python dict       
        id=p_data.get('id',None) #to check if key 'id' is there in p_data otherwise id=None
        if id is None:
            json_data=json.dumps({'message':'Id is required to perform Updation'})
            return self.render_to_httpresp_status(json_data,status=404)

        #if id is not none then check if that id is avialble in the database or not
        emp=get_emp_by_id(id) #utility func to check id is available
        if emp is None:
            json_data=json.dumps({'message':'Record is not available'})
            return self.render_to_httpresp_status(json_data,status=404)

        # if emp with id is avialble in the database
        original_data={'eno':emp.eno,'ename':emp.ename,'esal':emp.esal,'eaddr':emp.eaddr}
        # del p_data['id']
        original_data.update(p_data)  #update the original dict with new dict values
        #update is there so need form instance
        form=EmployeeForm(original_data,instance=emp) #instance=emp is imp so it will update existing record instead of creating new one
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'message':'Record updated successfully'})
            return self.render_to_httpresp_status(json_data)
        
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_httpresp_status(json_data,status=404)
        
    def delete(self,request,*args,**kwargs):
        data=request.body #take data send by client app
        valid_json=is_valid_data(data)
        if not valid_json:
            json_data=json.dumps({'message':'Not valid data'})
            return self.render_to_httpresp_status(json_data,status=404)
        p_data=json.loads(data)        
        id=p_data.get('id',None)
        if id is not None:
            emp=get_emp_by_id(id)
            if emp is None:
                json_data=json.dumps({'message':'Record not available'})
                return self.render_to_httpresp_status(json_data,status=404)
            
            #when emp is there with matched id
            del_item=emp.delete()  #it provides tuple (a,b)
            # t=(1, {'api.Employee': 1})---->status,deleted_item
            status,deleted_item=del_item  
            if status == 1: #if 1 means successful
                json_data=json.dumps({'message':'Record deleted successfully'})
                return self.render_to_httpresp_status(json_data)            
            #if not status=1
            json_data=json.dumps({'message':'Unable to delete .Please try agian'})
            return self.render_to_httpresp_status(json_data,status=404)
        
        #if id is None.
        json_data=json.dumps({'message':'Id is not provided so couldnot delete'})
        return self.render_to_httpresp_status(json_data,status=404)
        
        
        
        



        



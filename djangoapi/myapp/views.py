from django.shortcuts import render
from django.views.generic import View
from .utility import *
from .mixins import HttpResponseMixin,SerializeMixin
import json
from .models import Student
from .forms import StudentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
@method_decorator(csrf_exempt,name='dispatch')
class StudentCRUD_cbv(View,HttpResponseMixin,SerializeMixin):
    def get(self,request,*args,**kwargs):
        #id may be or may not be there from client
        data=request.body
        valid_data=is_valid_json(data)
        if not valid_data:
            json_data=json.dumps({'message':'Please send Valid json data'})
            return self.render_to_http_response(json_data,status=404) #client error

        p_data=json.loads(data)
        id=p_data.get('id',None)

        if id is not None:
            student=get_student_by_id(id)
            if student is None:
                json_data=json.dumps({'message':'No matched record found'})
                return self.render_to_http_response(json_data,status=404)
            
            #if student is available then student obj data -->json data
            json_data=self.serialize([student,])
            return self.render_to_http_response(json_data)

        #if no id then all students data should client app reeive
        all_students=Student.objects.all()
        json_data=self.serialize(all_students)
        return self.render_to_http_response(json_data)
    
    def post(self,request,*args,**kwargs):
        data=request.body
        valid_data=is_valid_json(data)
        if not valid_data:
            json_data=json.dumps({'message':'Please send Valid json data'})
            return self.render_to_http_response(json_data,status=404) #client error
        
        student_data=json.loads(data)
        form=StudentForm(student_data)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'message':'Record created successfully'})
            return self.render_to_http_response(json_data)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=404)

    def put(self,request,*args,**kwargs):
        data=request.body
        valid_data=is_valid_json(data)
        if not valid_data:
            json_data=json.dumps({'message':'Please send Valid json data'})
            return self.render_to_http_response(json_data,status=404) #client error
        
        student_data=json.loads(data)
        id=student_data.get('id',None)
        if id is None:
            json_data=json.dumps({'message':'Please provide id to update record'})
            return self.render_to_http_response(json_data,status=404) #client error
        
        student=get_student_by_id(id)
        if student is None:
            json_data=json.dumps({'message':'No matched record found'})
            return self.render_to_http_response(json_data,status=404) #client error
        
        original_student_data={'name':student.name,
        'rollno':student.rollno,
        'marks':student.marks,
        'gm':student.gm,
        'gf':student.gf}

        original_student_data.update(student_data)
        form=StudentForm(original_student_data,instance=student)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'message':'Record updated successfully'})
            return self.render_to_http_response(json_data)
        
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=404)

    def delete(self,request,*args,**kwargs):
        data=request.body #get the sent data
        valid_data=is_valid_json(data) #check validation
        if not valid_data:#if data is not valid
            json_data=json.dumps({'message':'Please provide valid json data'})
            return self.render_to_http-response(json_data,status=404)
        student_data=json.loads(data) #if valid data get dict object
        id=student_data.get('id',None) #check if id is there or it is None
        if id is None:
            json_data=json.dumps({'message':'Please provide Record Id to delete it'})
            return self.render_to_http-response(json_data,status=404)
        student=get_student_by_id(id) #if id is tehre check record is there or not
        if student is None:
            json_data=json.dumps({'message':'Matched record not found'})
            return self.render_to_http_response(json_data,status=404)
        
        status,data=student.delete() #if record is available delete it
        if status==1:
            json_data=json.dumps({'message':'Record deleted successfully'})
            return self.render_to_http_response(json_data)
        json_data=json.dumps({'message':'Something went wrong please try again'})
        return self.render_to_http-response(json_data,status=404)
        



        


        
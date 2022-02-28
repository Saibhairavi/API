
from django.http import HttpResponse
import json
from django.core.serializers import serialize

class HttpResponseMixin(object):
    def render_to_http_response(self,data,status=200):
        return HttpResponse(data,content_type='application/json',status=status)

class SerializeMixin(object):
    def serialize(self,qs):
        json_data=serialize('json',qs,fields=['name','rollno','marks','gm','gf'])
        dict_data=json.loads(json_data)
        all_emp_data=[]
        for obj in dict_data:
            all_emp_data.append(obj['fields'])        
        final_json_data=json.dumps(all_emp_data)
        return final_json_data
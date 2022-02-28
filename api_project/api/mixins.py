from django.http import HttpResponse
from django.http import HttpResponse
from django.core.serializers import serialize
import json
class HttpResponseMixin(object):  #mixin class containes instance methods
    #always extends object class
    def render_to_httpresponse(self,json_data):
        return HttpResponse(json_data,content_type='application/json')
    def render_to_httpresp_status(self,json_data,status=200):
        return HttpResponse(json_data,content_type='application/json',status=status)

class SerializeMixin(object):
    def serialize(self,qs):
        json_data=serialize('json',qs,fields=['eno','ename','eaddr'])
        #fields for whcih columns to display in json output
        dict_data=json.loads(json_data)
        all_emp_data=[]
        for obj in dict_data:
            all_emp_data.append(obj['fields'])        
        final_json_data=json.dumps(all_emp_data)
        return final_json_data

# total rest api,everywhere mixin mixin mixin used

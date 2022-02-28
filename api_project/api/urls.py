from django.urls import path
from . import views
urlpatterns = [
    path('api/',views.employee_data,name='employee_data'), #function based view

    path('api_json/',views.json_resp.as_view(),name='json_resp'),
    #class based view into function based view---.as_view

    # path('get_emp/',views.EmployeeDetail.as_view(),name='getemp'),
    path('get_emp/<int:id>/',views.EmployeeDetail.as_view(),name='getemp'),
    path('get_all_emp/',views.EmployeeListDetails.as_view(),name='getallemp'),

    # _________________________________________________________________________________

    #for single endpoint
    path('api_api/',views.EmployeeCRUD_cbv.as_view(),name='EmployeeCRUD_cbv')
    #so all parter app we will provide this standalone endpoint ,easyily 
]

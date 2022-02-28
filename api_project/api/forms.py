from pyexpat import model
from django import forms
from .models import Employee

#todo check for other validations
class EmployeeForm(forms.ModelForm):
    def clean_esal(self):
        #Need to validate salary.
        inputsal=self.cleaned_data['esal']
        if inputsal<1000:
            raise forms.ValidationError('The minimum sal should be 1000')
        return inputsal
    class Meta:
        model=Employee
        #table name 
        fields='__all__'
        #to get all the fields from db table.
    

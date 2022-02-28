from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    def clean_marks(self):
        inmarks=self.cleaned_data['marks']
        if inmarks<35:
            raise forms.ValidationError('Marks should be >35')
        return inmarks
    class Meta:
        model = Student
        fields = '__all__'

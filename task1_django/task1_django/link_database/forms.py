from django import forms
from .models import Student, University
from django.forms import TextInput, DateTimeInput, Textarea

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["FIO", "born_date", "get_in_year", "university"]

        widgets = {"FIO": TextInput(attrs={"placeholder": "FIO"}),
                   "born_date": DateTimeInput(attrs={"placeholder": "YYYY-MM-DD"}),
                   "get_in_year": DateTimeInput(attrs={"placeholder": "YYYY-MM-DD"}),
                   }
    #FIO = forms.CharField(initial='Иванов Иван Иванович')
    #born_date = forms.DateField(help_text='Format: YYYY-MM-DD')
    #get_in_year = forms.DateField(help_text='Format: YYYY-MM-DD')
    #university = forms.DecimalField(initial=9999)

# forms.Form
class UniversityForm(forms.ModelForm):

    class Meta:
        model = University
        fields = ["full_name", "short_name", "foundation_date"]

        widgets = {"full_name": TextInput(),
                   "short_name": TextInput(),
                   "foundation_date": DateTimeInput(attrs={"placeholder": "YYYY-MM-DD"}),
                   }
    #full_name = forms.CharField()
    #short_name = forms.CharField()
    #foundation_date = forms.DateField(help_text='Format: YYYY-MM-DD')


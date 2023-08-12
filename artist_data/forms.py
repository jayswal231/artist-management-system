
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email',  'phone', 'dob', 'gender', 'address']
        widgets = {
            'password': forms.PasswordInput(),  
        }


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')

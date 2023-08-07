
from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password', 'phone', 'dob', 'gender', 'address']
        widgets = {
            'password': forms.PasswordInput(),  
        }
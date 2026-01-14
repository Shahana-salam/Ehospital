# accounts/forms.py
from django import forms

from doctorapp.models import Doctor
from .models import  User

class DoctorForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True
    )
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Doctor
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'specialization',
            'phone',
            'location'
        ]

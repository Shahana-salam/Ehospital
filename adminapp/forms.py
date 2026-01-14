from django import forms

from facility.models import Department, Location


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'location']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department name'
            }),
            'location': forms.Select(attrs={
                'class': 'form-control'
            }),
        }



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location name'
            }),

        }
from django import forms

from facility.models import Resource
from patientapp.models import HealthResource


class HealthResourceForm(forms.ModelForm):
    class Meta:
        model = HealthResource
        fields = ['title', 'content', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Resource Content', 'rows': 4}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional Link'}),
        }



class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'department', 'quantity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

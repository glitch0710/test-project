from django.forms import ModelForm, TextInput, Select, Textarea
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender','address','income_annual']
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
            }),
            'last_name': TextInput(attrs={
                'class': "form-control"
            }),
            'gender': Select(attrs={
                'class': "form-control"
            }),
            'address': Textarea(attrs={
                'class': "form-control",
                'rows': "3"
            }),
            'income_annual': TextInput(attrs={
                'class': "form-control"
            })
        }

from dataclasses import field, fields
from statistics import mode
from django.forms import ModelForm, TextInput, Select, Textarea, NumberInput, FileInput
from .models import Profile, UsersAreaInfo, Farmer, ProfileAttachments, AreaCrop, FarmerDependents


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender',]
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
        }


class FarmerForm(ModelForm):
    class Meta:
        model = Farmer
        fields = [
            'first_name', 
            'last_name', 
            'middle_name',
            'gender',
            'contact_no',
            'tin',
            'philhealth',
            'sss',
            'pagibig',
            'birthdate',
            'civil_status',
            'nationality',
            'spouse',
        ]

        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
            }),
            'last_name': TextInput(attrs={
                'class': "form-control"
            }),
            'middle_name': TextInput(attrs={
                'class': "form-control"
            }),
            'gender': Select(attrs={
                'class': "form-control"
            }),
            'contact_no': TextInput(attrs={
                'class': "form-control"
            }),
            'birthdate': TextInput(attrs={
                'class': "form-control",
                'placeholder': "mm/dd/yyyy"
            }),
            'civil_status': Select(attrs={
                'class': "form-control"
            }),
            'nationality': TextInput(attrs={
                'class': "form-control"
            }),
            'tin': TextInput(attrs={
                'class': "form-control"
            }),
            'philhealth': TextInput(attrs={
                'class': "form-control"
            }),
            'sss': TextInput(attrs={
                'class': "form-control"
            }),
            'pagibig': TextInput(attrs={
                'class': "form-control"
            }),
            'spouse': TextInput(attrs={
                'class': "form-control"
            }),
        }


class FarmerAttachmentsForm(ModelForm):
    class Meta:
        model = ProfileAttachments
        fields = [
            'id_picture',
            'cedula',
            'brgy_clearance',
            'tax_dec',
            'valid_id_one',
            'valid_id_two'
        ]


class FarmerDependentsForm(ModelForm):
    class Meta:
        model = FarmerDependents
        fields = [
            'dependent_name',
            'age',
        ]

        widgets = {
            'dependent_name': TextInput(attrs={
                'class': "form-control",
            }),
            'age': NumberInput(attrs={
                'class': "form-control",
            }),
        }


class UserAreaTechnicalForm(ModelForm):
    class Meta:
        model = UsersAreaInfo
        fields = [
            'farmer_id',
            'total_area',
            # 'crop_planted',
            # 'remarks',
            'area_coordinates',
            'profile_field',
            'soil_ph',
        ]

        widgets = {
            'farmer_id': Select(attrs={
                'class': "form-control"
            }),
            'total_area': TextInput(attrs={
                'class': "form-control"
            }),
            # 'crop_planted': Select(attrs={
            #     'class': "form-control"
            # }),
            # 'remarks': Textarea(attrs={
            #     'class': "form-control",
            #     'rows': "3"
            # }),
            'profile_field': TextInput(attrs={
                'class': "form-control",
            }),
            'soil_ph': NumberInput(attrs={
                'class': "form-control",
            }),
        }


class AreaCropForm(ModelForm):
    class Meta:
        model = AreaCrop
        fields = [
            'crop_planted',
            'status',
            'remarks',
        ]

        widgets = {
            'crop_planted': Select(attrs={
                'class': "form-control"
            }),
            'status': TextInput(attrs={
                'class': "form-control",
            }),
            'remarks': Textarea(attrs={
                'class': "form-control",
                'rows': "3"
            }),
        }


class UserAreaEngineerForm(ModelForm):
    class Meta:
        model = UsersAreaInfo
        fields = [
            'sketch_plan',
            'map',
            'google_earth',
        ]

class UserAreaForm(ModelForm):
    class Meta:
        model = UsersAreaInfo
        fields = [
            'farmer_id',
            'total_area',
            'crop_planted',
            'remarks',
            'sketch_plan',
            'map',
            'google_earth',
            'area_coordinates',
            'profile_field',
            'soil_ph',]

        widgets = {
            'farmer_id': Select(attrs={
                'class': "form-control"
            }),
            'total_area': TextInput(attrs={
                'class': "form-control"
            }),
            'crop_planted': Select(attrs={
                'class': "form-control"
            }),
            'remarks': Textarea(attrs={
                'class': "form-control",
                'rows': "3"
            }),
            # 'sketch_plan': FileInput(attrs={
            #     'class': "custom-file-input",
            #     'aria-describedby': "inputGroupFileAddon01",
            # }),
            # 'map': FileInput(attrs={
            #     'class': "custom-file-input",
            #     'aria-describedby': "inputGroupFileAddon02",
            # }),
            # 'google_earth': FileInput(attrs={
            #     'class': "custom-file-input",
            #     'aria-describedby': "inputGroupFileAddon03",
            # }),
            'profile_field': TextInput(attrs={
                'class': "form-control",
            }),
            'soil_ph': NumberInput(attrs={
                'class': "form-control",
            }),

        }

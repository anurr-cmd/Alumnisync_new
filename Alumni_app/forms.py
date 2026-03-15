from django import forms
from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']


from django import forms
class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = "__all__"
        exclude = ["role","user"]
        
        
        
from django import forms
from .models import Profile


class AlumniEditForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "profile_image",
            "roll_no",
            "email",
            "designation",
            "department",
            "join_year",
            "passout_year",
            "address",
            "current_job",
            "company",
            "location",
            "phone",
            "alternate_phone",
            "remarks",
        ]

        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
        }
        
        
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class AlumniCreateForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile

        fields = [
            "profile_image",
            "roll_no",
            "email",
            "designation",
            "department",
            "join_year",
            "passout_year",
            "address",
            "current_job",
            "company",
            "location",
            "phone",
            "alternate_phone",
            "remarks",
        ]

        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
        }
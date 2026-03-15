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
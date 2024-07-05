from django import forms
from .models import MudData,Rheogram,RheogramDate

class MudDataForm(forms.ModelForm):
    class Meta:
        model = MudData
        fields = "__all__"


class RheogramForm(forms.ModelForm):
    class Meta:
        model = Rheogram
        fields = "__all__"

class RheogramdateForm(forms.ModelForm):
    class Meta:
        model = RheogramDate
        fields = "__all__"
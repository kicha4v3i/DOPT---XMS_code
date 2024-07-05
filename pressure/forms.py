from django import forms
from .models import Pressure

class PressureForm(forms.ModelForm):
    class Meta:
        model = Pressure
        fields = "__all__"
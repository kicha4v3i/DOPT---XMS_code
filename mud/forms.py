from custom_auth.views import Companiesapprove
from django import forms
from .models import MudPump,MudPumpFlowRate,MudPumpData,MudPumpSpeed,PumpManufacturer,Pumps
from django.core.exceptions import ValidationError

class MudPumpForm(forms.ModelForm):
    class Meta:
        model = MudPump
        fields = "__all__"


class MudPumpDataForm(forms.ModelForm):
    class Meta:
        model = MudPumpData
        fields = "__all__"



class MudPumpSpeedForm(forms.ModelForm):
    class Meta:
        model = MudPumpSpeed
        fields = "__all__"


class MudPumpFlowRateForm(forms.ModelForm):
    class Meta:
        model = MudPumpFlowRate
        fields = "__all__"


class PumpManufacturerForm(forms.ModelForm):
    class Meta:
        model = PumpManufacturer
        fields = "__all__"
        widgets = {'company': forms.HiddenInput(),'status': forms.HiddenInput()}


class PumpsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PumpsForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Pumps
        fields = "__all__"
        widgets = {'company': forms.HiddenInput(),'status': forms.HiddenInput()}

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        company = cleaned_data.get("company")
        id = cleaned_data.get("id")
        if id:
            return 
        else:
            if Pumps.objects.filter(name=name,company=company).exists():
                raise ValidationError(
                "Name Already Exists"
                )
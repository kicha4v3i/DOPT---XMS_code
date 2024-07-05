

from django import forms
from wellphases.models import WellPhases,Casing


class CasingForm(forms.ModelForm):
    class Meta:
        model = Casing
        fields = "__all__"
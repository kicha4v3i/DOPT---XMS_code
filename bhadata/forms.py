from django import forms
from bhadata.models import BhaData,BhaElement,Drillcollers,Drillpipe,DrillpipeHWDP,Specifications,Differential_pressure


class BhaDataForm(forms.ModelForm):
    class Meta:
        model = BhaData
        fields = "__all__"


class BhaElementForm(forms.ModelForm):
    class Meta:
        model = BhaElement
        fields = "__all__"


class DrillcollersForm(forms.ModelForm):
    class Meta:
        model = Drillcollers
        fields = "__all__"


class DrillpipeForm(forms.ModelForm):
    class Meta:
        model = Drillpipe
        fields = "__all__"


class DrillpipeHWDPForm(forms.ModelForm):
    class Meta:
        model = DrillpipeHWDP
        fields = "__all__"

class SpecificationsForm(forms.ModelForm):
    class Meta:
        model = Specifications
        fields = "__all__"

class Differential_pressureForm(forms.ModelForm):
    class Meta:
        model = Differential_pressure
        fields = "__all__"
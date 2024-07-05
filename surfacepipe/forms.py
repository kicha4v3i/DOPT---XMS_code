from django import forms
from .models import SurfacePipe,SurfacePipeData


class SurfacePipeForm(forms.ModelForm):
    class Meta:
        model = SurfacePipe
        fields = "__all__"

class SurfacePipeDataForm(forms.ModelForm):
    class Meta:
        model = SurfacePipeData
        fields = "__all__"


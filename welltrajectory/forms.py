from django import forms
from .models import WellTrajectory

class WellTrajectoryForm(forms.ModelForm):
    class Meta:
        model = WellTrajectory
        fields = "__all__"
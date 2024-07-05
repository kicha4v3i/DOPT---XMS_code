from django import forms
from .models import Projects,ProjectUsers

class ProjectsForm(forms.ModelForm):
    # CHOICES = [('API','API'),('SI','SI'),('MIXED','MIXED API')]
    # unit=forms.CharField(label='Unit', widget=forms.RadioSelect(choices=CHOICES))
    class Meta:
        model = Projects
        fields = "__all__"
        widgets = {'status': forms.HiddenInput(),'created':forms.HiddenInput(),'created_by':forms.HiddenInput(),'company':forms.HiddenInput()}

class ProjectUsersForm(forms.ModelForm):
    class Meta:
        model = ProjectUsers
        fields = "__all__"
        widgets = {'status': forms.HiddenInput(),'project':forms.HiddenInput(),'role':forms.HiddenInput(),'created':forms.HiddenInput()}


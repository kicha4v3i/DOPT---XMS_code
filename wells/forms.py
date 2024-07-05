from django import forms
from .models import Wells,WellUsers
from projects.models import Projects,ProjectUsers,ProjectBlock,ProjectField

class WellsForm(forms.ModelForm):
    class Meta:
        model = Wells
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(WellsForm, self).__init__(*args, **kwargs)
        self.fields['block'] = forms.ModelChoiceField(
            queryset=ProjectBlock.objects.all()
        )
        self.fields['field'] = forms.ModelChoiceField(
            queryset=ProjectField.objects.all()
        )
class WellUsersForm(forms.ModelForm):
    class Meta:
        model = WellUsers
        fields = "__all__"


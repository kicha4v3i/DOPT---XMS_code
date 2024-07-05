from django import forms
from drillbitdata.models import DrillBit,DrillBitNozzle
from django.forms.formsets import formset_factory

class DrillBitForm(forms.ModelForm):
    class Meta:
        model = DrillBit
        fields = "__all__"

class DrillBitNozzleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DrillBitNozzleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control nozzle_size'

    class Meta:
        model = DrillBitNozzle
        fields = "__all__"
        widgets = {'company': forms.HiddenInput(),'drillbit': forms.HiddenInput(),'well': forms.HiddenInput(),'status': forms.HiddenInput()}

DrillBitNozzleFormset= formset_factory(DrillBitNozzleForm,extra=1)

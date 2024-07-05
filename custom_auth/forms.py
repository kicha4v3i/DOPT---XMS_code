from django import forms
from django.contrib.auth import get_user_model
from custom_auth.models import Companies

class SignupForm(forms.ModelForm):
    """user signup form"""
    password = forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(SignupForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['password'].required = False

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password','lastname','title','designation')


class LoginForm(forms.Form):
    """user login form"""
    # cin = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class AdminLoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class CompanySignupForm(forms.ModelForm):
    """user signup form"""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Companies
        fields = ('company_name', 'first_name', 'last_name','country', 'email','contact_no')
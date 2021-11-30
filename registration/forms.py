from django import forms
from django.db.models import fields
from .models import *
from django.forms import ModelForm

class RegistrationForm(ModelForm):
    class Meta:
        genders = [('Male','Male'), ('Female','Female'),('Others','Others')]
        model = users
        fields = '__all__'
        exclude = ('user_creation_date', 'last_login', 'is_authenticatedd')
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'birthdate': forms.DateInput(attrs={'type':'date', 'required':True}),
            'gender': forms.Select(choices=genders),
            'mobileno': forms.TextInput(),
            'password': forms.PasswordInput(),
            'username': forms.TextInput(),
            'profilepic': forms.FileInput(attrs={'accept':'image/*'}),
            }
    
    confirmpassword = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

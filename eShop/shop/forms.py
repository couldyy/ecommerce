from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class EmailContact(forms.Form):
    user_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #email_subject = forms.CharField(label='Тема письма', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #email_content = forms.CharField(label='Текст письма', widget=forms.TextInput(attrs={'class': 'form-control'}))

class emailSubscribe(forms.ModelForm):
    class Meta:
        model = UserEmails
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput()
        }

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:60%;'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:60%;'},))
    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name", "mobile", "password1", "password2")
        widgets = {
            "email": forms.EmailInput(attrs={'class': 'form-control', 'style': 'width:60%;'}),
            "username": forms.TextInput(attrs={'class': 'form-control', 'style': 'width:60%;'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'style': 'width:60%;'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control', 'style': 'width:60%;'}),
            "mobile": forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:60%;'}),
        }

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:60%;'}))
    class Meta:
        model = Account
        fields = ("email", "password")
        widgets = {
            "email": forms.EmailInput(attrs={'class': 'form-control', 'style': 'width:60%;'}),
        }

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise ValidationError('Invalid login')


class ChangeAccountDateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'mobile', 'email', 'address')

class MakeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'mobile', 'address', 'country', 'city', 'state', 'zip_code', 'product_quantity', 'payment_method')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
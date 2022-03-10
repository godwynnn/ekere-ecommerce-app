# from readline import parse_and_bind
from enum import unique
from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

class EkerePostForm(forms.ModelForm):
    # content=forms.TextInput(attrs={"placeholder": "write your post!!", "width":30})
    class Meta:
        model= Product
        fields=['title','content']

class UserForm(UserCreationForm):
    
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        model= User
        fields=['first_name','last_name','username','email','password1','password2']

        widgets={
            'first_name': forms.TextInput(attrs={'placeholder':'Enter Firstname'}),
            'last_name': forms.TextInput(attrs={'placeholder':'Enter Lastname'}),
            'username': forms.TextInput(attrs={'placeholder':'Enter Username'}),
            'email': forms.TextInput(attrs={'placeholder':'Enter Email'}),
            # 'password1': forms.PasswordInput(attrs={'placeholder':'Enter Password'}),
            # 'password2': forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),
        }

    def clean_data(self):
        password=self.cleaned_data.get('password').value()
        email=self.cleaned_data.get('email')
        query=User.objects.filter(password=password,email=email)
        if query.exists():
            raise ValidationError('Password or Email already taken')
        return password


class UserProfileform(forms.ModelForm):
    class Meta:
        model=Userprofile
        fields=['image']
      
    
class AddressForm(forms.ModelForm):
    class Meta:
        model= Address
        fields='__all__'
        exclude=['default','member_id','user']



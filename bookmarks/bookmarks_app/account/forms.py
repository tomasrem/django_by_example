from django import forms
from django.contrib.auth.models import User
from .models import Profile

# custom login form :)
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# custom registration form 
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat your password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username' , 'first_name', 'email']

    #password validation
    def clean_password2(self): # you can provide clean_<field name>(): method to any of your form field and this method is called when we call the is_valid() method
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password don't match")
        return cd['password2']


    #email validation
    def clean_email(self):
        data = self.cleaned_data['email'] # get the email from submited form 
        if User.objects.filter(email=data).exists(): # check if the user exist with given email 
            raise forms.ValidationError('Email already in use , please try another one or restore password for your account.') # if yes raise validation error
        return data # otherwise return the value of the form 


# form for editing user info
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)

        if qs.exists():
            if data == '':
                raise forms.ValidationError(' Please enter your new email adress ')
            else:
                raise forms.ValidationError(' Email already in use. ')
        return data

# form for editing profile info 
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth' , 'photo']
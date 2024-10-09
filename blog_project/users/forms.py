from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

class CreateProfileForm(forms.ModelForm):
    

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', ]

class ChangeUserForm(UserChangeForm):
    class Meta: 
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]

class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']



# class LoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput())
#     password = forms.CharField(widget=forms.PasswordInput())
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, EmployerProfile


class SeekerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class EmployerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password'] 
        
class ManagerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2'] 
        

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'company_name', 'location', 'company_website', 'company_description',
            'phone', 'email', 'facebook_link', 'twitter_link', 'google_link', 'linkedin_link', 'founded_date'
        ]
        widgets = {
            'founded_date': forms.DateInput(attrs={'type': 'date'}),
        }


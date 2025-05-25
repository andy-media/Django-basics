from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import User, School, Contestant, Coach

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name_of_school', 'region', 'location', 'school_head_name', 'school_contact']

class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['name', 'year_form']

ContestantFormSet = forms.inlineformset_factory(
    School, Contestant, form=ContestantForm, extra=4, can_delete=False
)

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['coach_type', 'name', 'contact_number']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
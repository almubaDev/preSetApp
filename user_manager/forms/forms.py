from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from ..models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'country', 'password1', 'password2')

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class CustomChangePasswordForm(PasswordChangeForm):
    class Meta:
        model: CustomUser
        fields = ('password1', 'password2')
        
class CustomResetPasswordForm(PasswordResetForm):
    class Meta:
        model: CustomUser
        fields = ('email')
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms.forms import CustomUserLoginForm, CustomUserCreationForm, CustomChangePasswordForm, CustomResetPasswordForm
from django.shortcuts import render, redirect



def user_home(request):
    return render(request, 'user_home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_home')
        else:
            return render(request, 'register.html', {
                'form' :  CustomUserCreationForm,
                'errors' : form.errors
            })
  
    return render(request, 'register.html', 
                  {'form':CustomUserCreationForm})

class CustomUserLoginView(LoginView):
    template_name = 'login.html'  
    form_class = CustomUserLoginForm


@method_decorator(login_required, name='dispatch' )
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    form_class = CustomChangePasswordForm

@method_decorator(login_required, name='dispatch' )
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    def get(self, *args, **kwargs):
        return redirect('logout')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    form_class = CustomResetPasswordForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'reset_password_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
   
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_completed.html'
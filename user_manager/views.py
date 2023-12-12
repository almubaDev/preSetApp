from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms.forms import CustomUserLoginForm, CustomUserCreationForm, CustomChangePasswordForm, CustomResetPasswordForm
from .models import CustomUser


def user_home(request):
    return render(request, 'user_manager/user_home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            return redirect('user_home')
        else:
            return render(request, 'user_manager/register.html', {
                'form' :  CustomUserCreationForm(),
                'errors' : form.errors
            })
  
    return render(request, 'user_manager/register.html', 
                  {'form': CustomUserCreationForm()})



class CustomUserLoginView(LoginView):
    template_name = 'user_manager/login.html'  
    form_class = CustomUserLoginForm


@method_decorator(login_required, name='dispatch' )
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'user_manager/change_password.html'
    form_class = CustomChangePasswordForm


@method_decorator(login_required, name='dispatch' )
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    def get(self, *args, **kwargs):
        return redirect('logout')


# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'password_reset.html'
#     form_class = CustomResetPasswordForm



def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = CustomUser.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = "Reestablecimiento de contraseña"
                    #email_template_name = 'password_reset_message.txt'
                    email_template_name = 'user_manager/password_reset_message.html'
                    parameters = {
                        'email': user_email,
                        'site_name': 'Preset web App',
                        'fullname': user.full_name,
                        'protocol': 'http',
                        'domain': '127.0.0.1:8000',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user)
                    }
                    
                    email_content= render_to_string(email_template_name, parameters)
                    email= EmailMessage(
                        subject=subject,
                        body=email_content,
                        to=[user.email]
                    )
                    email.content_subtype = 'html'
                    try:
                        email.send(fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done') 
    else:
        password_form = PasswordResetForm()

        context = {
            'password_form': password_form
        }
        return render(request,'user_manager/password_reset.html', context)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user_manager/reset_password_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_manager/password_reset_confirm.html'
   

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user_manager/password_reset_completed.html'


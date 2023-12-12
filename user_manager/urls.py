from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView,  PasswordResetConfirmView, PasswordResetCompleteView
from . import views


urlpatterns = [
    path('', views.user_home, name='user_home'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Agrega otras rutas según sea necesario
    
]

"""
urlpatterns = [
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('logout/', CustomUserLogoutView.as_view(), name='logout'),
    path('signup/', CustomUserSignUpView.as_view(), name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Agrega otras rutas según sea necesario
]
En este ejemplo:

CustomUserLogoutView es una vista basada en clases que maneja la acción de cierre de sesión.
CustomUserSignUpView es una vista basada en clases que maneja la acción de registro de nuevos usuarios.
auth_views.PasswordChangeView maneja la acción de cambio de contraseña.
auth_views.PasswordChangeDoneView maneja la acción después de cambiar la contraseña.
auth_views.PasswordResetView maneja la acción de solicitud de restablecimiento de contraseña.
auth_views.PasswordResetDoneView maneja la acción después de solicitar el restablecimiento de contraseña.
auth_views.PasswordResetConfirmView maneja la acción de confirmación de restablecimiento de contraseña.
auth_views.PasswordResetCompleteView maneja la acción después de confirmar el restablecimiento de contraseña.
"""
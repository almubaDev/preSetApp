from django.urls import path
from . import views
urlpatterns = [
    path('password_generator', views.password_generator, name='password_generator')
]

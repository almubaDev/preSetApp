from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('send_email/', include('send_email.urls')),
    path('user/', include('user_manager.urls')),
    path('password_generator/', include('password_generator.urls')),
]


# Custom User Manager App

Esta es una aplicación simple en Django para configurar un usuario completamente personalizado, incluido la relación con permisos y gurpo. Además se han creado urls y vistas personalizadas para gestionar todo el procesos en elación a un usario, registro, login, logout, cambio de contraseña y reseteo de contraseña.

# Instrucciones de instalación e implementación

1. Copie y pegue el directorio `user_manager` en el directorio raiz de su proyecto Django, como cualquier otra aplicaci+on creada en el proyecto.

2. En su archivo settings.py de su proyecto Django,  en el apartado de aplicaciones añada 'user_manager.apps.UserManagerConfig'.
```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'send_email.apps.SendEmailConfig',
        'home.apps.HomeConfig',
        'user_manager.apps.UserManagerConfig', #Como en este ejemplo
    ]
```
* ### Nota
    * Puede comporbar la si la aplicación se ha instalado correctamente ejecutado en la terminal el comando `python manage.py check usenager`,  si todo ha salido bien devolverá `System check identified no issues (0 silenced)`, de no ser el caso verifique si el nombre escrito en la    lista INSTALLED_APPS de su settings.py este correctamente escrita y coincida con el nombre `user_manager`.

3. En el archvio urls.py de su proyecto Django incluya las urls de user_manager `path('user/', include('user_manager.urls')),`.
```python
    from django.contrib import admin
    from django.urls import path, include   

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('home.urls')),
        path('user/', include('user_manager.urls')), #Incluirá las urls de la aplicación user_manager, a partir de del path "user/".
    ]
```
* ### Nota
    * Es importante tener configurado el envio de emails en el settings.py de tu proyecto, para así poder gestionar el reseteo decontraseñas    de usuario.
        ```python
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'smtp.tuproveedor.com'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = 'remitente@tuproveedor.com'
        EMAIL_HOST_PASSWORD = 'Contraseña de aplicación otorgada por tuproveedor.com'
        ```
    * Si necesita más orientación lee el readme.md de la aplicación send_email en este mismo repositorio. [Configuración envío de emails]       (https://github.com/almubaDev/preSetApp/blob/main/send_email/readme.md)

4. Modifica el modelo según lo que necesites, colocando los campos que estimes comvenientes, ten en cuenta que los que vienen por defecto estan diseñado sin el establecimiento de un username y para terminos técnios el username será el email del usuario. PAra más detalles lee la sección Modelo del apartado Documentación de esta lectura.

5. Ejecuta en la terminal el comando `python manage.py migrate`. Si todo ha salido bien ha de mostrar en consola el siguiente mensaje:
```Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, user_manager     
Running migrations:
  Applying user_manager.0001_initial... OK
```
Si aún no haz hecho las migraciones iniciales porbablemente la respuesta sea más larga, solo asegurate que `Applying user_manager.0001_initial... OK` aparezca, tambien puedes corroborar en tu base de datos si aparecen las siguientes tablas:
`user_manager_customuser`
`user_manager_customuser_groups`
`user_manager_customuser_user_permissions`

También verás que en el administrador de Django `/admin/` se ha agregado una sección con el nombre de la aplicación USER MANAGER y su modelo Custom users, y que de la sección AUTENTICACIÓN Y AUTORIZACIÓN ha desaparecido el modelu Users. 


# Documentación

## Modelos `models.py`
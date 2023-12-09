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
    * Si necesita más orientación lee el readme.md de la aplicación send_email en este mismo repositorio. [Configuración envío de emails](https://github.com/almubaDev/preSetApp/blob/main/send_email/readme.md)

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

## Modelo `models.py`

```python
    class CustomUserManager(BaseUserManager):
```
* BaseUserMAnager es una clase base proporcioada por Django para la gestión de usuarios, y extendemos sus funcionalidades a nuesta clase personalizada CustomUserManager.


```python
    if not email:
        raise ValueError('El campo "email" es obligatorio.')
```
* La función create_user debe recibir como argumentos un email, una password que se configurará como None por defecto en caso de no asignar una, se debe tener en cuenta que la contraseña será exigida igualmente, ya que no permitirá el campo vacío o que no se cumplan los parametros básico de extención y formato, alo anterior se suma una cantidad indeterminada de campos (**Kwargs formato disccionario) que se deseen añadir, también se condiciona el ingreso de un email, al no hacerlo se levantará una excepción.


```python
    email = self.normalize_email(email)
```
* La normalización del email campo Asegura que esté en un formato estandarizado, garantizando la unifromidad en la base de datos. 


```python
    user = self.model(email=email, **extra_fields)
```
*Crea una instancia del modelo usuario con su respectivo email y campos personalizados, sin el password ya que este necesita un paso previo antes de ser integrada a la instancia.


```python
    user.set_password(password)
```
*El método cifra y almacena la contraseña de forma segura.


```python
    user.save(using=self._db)
```
*Conecta a la base de datos y guarda la instancia de usuario que se ha creado.


```python
    return user
```
* Retorna la instancia recién creada para seguir trabajando con ella.


```python
    def create_superuser(self, email, password=None, **extra_fields):
```
* La función crea un súper usuario siguiendo la misma lógica de parametros que  `create_user`.


```python
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_staff', True)
```
*Se crean y configuran por defecto los atributos `is_superuser` e `is_staff` en `True`.


```python
    if extra_fields.get('is_staff') is not True:
        raise ValueError('Superuser debe tener is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
        raise ValueError('Superuser debe tener is_superuser=True.')
```
* Realiza la comporbación del valor True en ambos atributos, de no ser así levantará sus respectivas excepciones, esto es importante ya que se necesita de los permisos necesarios para realizar diversas acciones y Django reconoce estos campos para autorizarlas (Por ejemplo al panel de administación de Django), entro otras razones. 


```python
    return self.create_user(email, password, **extra_fields)
```
* De cumplirse todos los requemientos, la función retornará un usuario con los permisos necesarios, para crear el usuario hará uso de la función `create_user`definida previamente. 


```python
    class CustomUser(AbstractBaseUser, PermissionsMixin):

```
* La clase define al usuario personalizado. hereda de `AbstractBaseUser` que proporciona una funcionalidad básica para la creación de un usuario personalizado, `PermissionsMixin` agrega atributos y métodos para trabajar con permisos.


```python
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to.'),
        related_name='custom_users_groups'  # Elige un nombre personalizado
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='custom_users_permissions'  # Elige un nombre personalizado
    )
```
* El atributo `groups` `user_permissions` y  crea una relación de muchos a mucho con el modelo Group o Permission propios de Django, entendiendo que un usuario puede pertenecer a multiples grupos o poseer diversos permiso, como también que cada grupo o permiso puede integrar muchos usuarios.
* `Group` o `Permission` permite que mediante el nombre del objeto relacionado Group accede al usuarios pertenecientes a él, `Group.custom_users_groups.all()` o `Permission.custom_users_permissions`.   
* `verbose_name` es un atributo opcional que proprociona una etiqueta descriptiva al campo.
* `blank=True` Indica y permite que el campo pueda estar en blanco en los formularios de creación del usuario personalizado, en este contexto indica que el usuario puede pertener a cero o más grupos.
* `help_text` Proporciona un mensaje de ayuda ha mostarse en los formularios, indica a que refiere el campo las condiciones que ha de tener para cumplimentarlo a cabalidad.
* `related_name` Proporciona un nombre personalizado para la relación inversa del modelo.


```python
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
```
* Los campos requeridos para crear un usuario, por tanto, la información que solicitaremos y almacenaremos en la base de datos. 
* `is_active` permite activar o desactivar a un usuario dentro de nuestra aplicación si necesidad de eliminarlo de la base de datos, por tanto conservará los datos relacionados a su cuenta en caso de quere volver a activarse.
* `is_staff` permite darle un grado mayor de permisos a la instancia del usuario en particular, pudiendo acceder a la consola de administación entre otros.
* ` date_joined` alamcena la fecha de creación del usuario. El atributo `auto_now_add=True` establece la hora y la fecha actual en el momento en que se crea el usuario de forma automática, por tanto, este campo no debe ser cumplimentado desde el formulario de creación de usuario. 


```python
    objects = CustomUserManager()
```
* Proporsion un gestor personalizado al modelo usuario, en este caso lo hará mediante la asignación la clase `CustomUserManager` que hemos configurado al principio, la cuál de fine cómo se gestionan los usuarios. 



```python
    USERNAME_FIELD = 'email'
```
* Especifica que se usara el campo de email como nombre de usuario al acceder al modelo usuario, un ejemplo practico es que podrá iniciar sesión con el email y la contraseña. 


```python
    REQUIRED_FIELDS = []
```
* La lista vacía indca que no requiere de ningún campo adicional para la creación de un usario más allá del email y password. Esto no evita que gestionemos la logica necesaria en nuestros campos, vistas o formularios para exigir al usuario el ingreso del resto de los datos referente los campos.


```python
    def __str__(self):
        return self.email

```
* El metodo devuelve una el email del usuario como representación del objeto, haciendolo más legible en impresión por consola o su visulización en el administrador de Django.


```python
```
```python
```
```python
```
```python
```
# Custom User Manager App

Esta es una aplicación simple en Django para configurar un usuario completamente personalizado, incluidas la relaciones con los modelos de permisos y grupos. Además, se han creado rutas y vistas personalizadas para gestionar todo el procesos en relación a la gestión de usuarios, registro, inicio de sesión, cierre de sesión, cambio de contraseña y reestablecimiento de contraseña.


# Instrucciones de instalación e implementación

1. Copie y pegue el directorio `user_manager` en el directorio raiz de su proyecto Django, como cualquier otra aplicación creada en el proyecto.

2. En el archivo settings.py de su proyecto Django, en el apartado de aplicaciones añada 'user_manager.apps.UserManagerConfig'.
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
    * Puede comporbar la si la aplicación se ha instalado correctamente ejecutado en la terminal el comando `python manage.py check user_manager`, si todo ha salido bien devolverá `System check identified no issues (0 silenced)`, de no ser el caso verifique si el nombre escrito en la lista INSTALLED_APPS de su settings.py esté correctamente escrito y coincida con el nombre `user_manager.apps.UserManagerConfig`.

3. En el archivo urls.py de su proyecto Django incluya las urls de user_manager `path('user/', include('user_manager.urls')),`
```python
    from django.contrib import admin
    from django.urls import path, include   

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('user/', include('user_manager.urls')), #Incluirá las urls de la aplicación user_manager, a partir de del path "user/".
    ]
```
* ### Nota
    * Es importante tener configurado el envío de emails en el archivo settings.py de tu proyecto, para así poder gestionar el reseteo decontraseñas de usuario.
        ```python
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'smtp.tuproveedor.com'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = 'remitente@tuproveedor.com'
        EMAIL_HOST_PASSWORD = 'Contraseña de aplicación otorgada por tuproveedor.com'
        ```
    * Si necesita más orientación lee el readme.md de la aplicación send_email en este mismo repositorio. [Configuración envío de emails](https://github.com/almubaDev/preSetApp/blob/main/send_email/readme.md)

4. Modifica los modelos en models.py según lo que necesites, colocando los campos que estimes convenientes, ten en cuenta que los campos que vienen estan diseñados sin el establecimiento de un campo username y para términos técnios el username será el email del usuario. Para más detalles lee la sección Modelo del apartado Documentación de esta lectura.

5. Ejecuta en la terminal el comando `python manage.py migrate`. Si todo ha salido bien ha de mostrar en consola el siguiente mensaje:
```Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, user_manager     
Running migrations:
  Applying user_manager.0001_initial... OK
```
Si aún no haz hecho las migraciones iniciales probablemente la respuesta sea más larga, solo asegurate que `Applying user_manager.0001_initial... OK` aparezca, también puedes corroborar en tu base de datos si aparecen las siguientes tablas:
`user_manager_customuser`
`user_manager_customuser_groups`
`user_manager_customuser_user_permissions`

También verás que en el administrador de Django `/admin/` se ha agregado una sección con el nombre de la aplicación USER MANAGER y su modelo Custom users, y que de la sección AUTENTICACIÓN Y AUTORIZACIÓN ha desaparecido el modelo Users. 


# Documentación

## Modelo `models.py`

```python
    class CustomUserManager(BaseUserManager):
```
* `BaseUserMAnager` es una clase base proporcioada por Django para la gestión de usuarios, y extendemos sus funcionalidades a nuesta clase personalizada `CustomUserManager`.


```python
    if not email:
        raise ValueError('El campo "email" es obligatorio.')
```
* La función create_user debe recibir como argumentos un email, una password que se configurará como None por defecto en caso de no asignar una, se debe tener en cuenta que la contraseña será exigida igualmente, ya que no permitirá el campo vacío o que no se cumplan los parametros básico de extención y formato, a lo anterior se suma una cantidad indeterminada de campos (**Kwargs formato diccionario) que se deseen añadir, también se condiciona el ingreso de un email, al no hacerlo se levantará una excepción.


```python
    email = self.normalize_email(email)
```
* La normalización del campo email asegura que esté en un formato estandarizado, garantizando la unifromidad en la base de datos. 


```python
    user = self.model(email=email, **extra_fields)
```
* Crea una instancia del modelo usuario con su respectivo email y campos personalizados, sin el password ya que este necesita un paso previo antes de ser integrada a la instancia.


```python
    user.set_password(password)
```
* El método cifra y almacena la contraseña de forma segura.


```python
    user.save(using=self._db)
```
* Conecta a la base de datos y guarda la instancia de usuario que se ha creado.


```python
    return user
```
* Retorna la instancia recién creada para seguir trabajando con ella.


```python
    def create_superuser(self, email, password=None, **extra_fields):
```
* La función crea un súper usuario siguiendo la misma lógica de parametros que `create_user`.


```python
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_staff', True)
```
* Se crean y configuran por defecto los atributos `is_superuser` e `is_staff` en `True`.


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
* De cumplirse todos los requerimientos, la función retornará un usuario con los permisos necesarios, para crearlo hará uso de la función `create_user` definida previamente. 


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
* Los atributo `groups` y `user_permissions` crean una relación de muchos a muchos con el modelo Group o Permission propios de Django, entendiendo que un usuario puede pertenecer a multiples grupos o poseer diversos permiso, como también que cada grupo o permiso puede integrar muchos usuarios.
* `Group` o `Permission` permite que mediante el nombre del objeto relacionado Group accede al usuarios pertenecientes a él, `Group.custom_users_groups.all()` o `Permission.custom_users_permissions.all()`.   
* `verbose_name` es un atributo opcional que proprociona una etiqueta descriptiva al campo.
* `blank=True` Indica y permite que el campo pueda estar en blanco en los formularios de creación del usuario personalizado, en este contexto indica que el usuario puede pertener a cero o más grupos.
* `help_text` Proporciona un mensaje de ayuda ha mostarse en los formularios, indica a que refiere el campo y las condiciones que ha de tener para cumplimentarlo a cabalidad.
* `related_name` Proporciona un nombre personalizado para la relación inversa del modelo.


```python
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
```
* Los campos requeridos para crear un usuario, por tanto, la información que solicitaremos y almacenaremos en la base de datos. Es aquí donde debe crear los campos según sus necesidades.
* `is_active` permite activar o desactivar a un usuario dentro de nuestra aplicación si la necesidad de eliminarlo de la base de datos, por tanto se conservarán los datos relacionados a su cuenta en caso de querer volver a activarse.
* `is_staff` permite darle un grado mayor de permisos a la instancia del usuario en particular, pudiendo acceder a la consola de administación entre otros.
* ` date_joined` almacena la fecha de creación del usuario. El atributo `auto_now_add=True` establece la hora y la fecha actual del momento en que se crea el usuario de forma automática, por tanto, este campo no debe ser cumplimentado desde el formulario de creación de usuario. 


```python
    objects = CustomUserManager()
```
* Proporsiona un gestor personalizado al modelo usuario, en este caso lo hará mediante la asignación la clase `CustomUserManager` que hemos configurado al principio del archivo, la cuál define cómo se gestionan los usuarios. 



```python
    USERNAME_FIELD = 'email'
```
* Especifica que se usará el campo de email como `username` al acceder al modelo usuario, un ejemplo práctico es que podrá iniciar sesión con el email y la contraseña. 


```python
    REQUIRED_FIELDS = []
```
* La lista vacía indica que no requiere de ningún campo adicional para la creación de un usario más allá del email y el password. Esto no evita que gestionemos la logica necesaria en nuestros campos, vistas o formularios para exigir al usuario el ingreso del resto de los datos referente los campos personalizados.


```python
    def __str__(self):
        return self.email

```
* El metodo devuelve una el email del usuario como representación del objeto, haciendolo más legible en la impresión por consola o su visulización en el administrador de Django.



## Formularios `forms.py
```python
    class CustomUserCreationForm(UserCreationForm):
```
```python
    class CustomUserLoginForm(AuthenticationForm):
```
```python
    class CustomChangePasswordForm(PasswordChangeForm):
```
```python
    class CustomChangePasswordForm(PasswordChangeForm):
```
* Se han creado cuatro fomularios personalizados para recibir información por parte del usuario y almacernarla en la base de datos, todos heredan de los formularios originales de la gestión de usuario, como las funciones son Crear usuario, Iniciar sesión, Solicitar el cambio de contraseña, Modificar contraseña.

```python
    class Meta:
        model: CustomUser
        fields = ('campo1', 'campo2')
```
* La clase Meta se estable como modelo al cual se relaciona el formulario `CustomUser`, lo que permite trabajar con el usuario personalizado, fields lista los campos requeridos para cumplir la función especifica de cada formulario. 

`
## Vistas `views.py`

```python
    def register(request):
```
* Renderiza  mediante el metodo GET el template con el fomrulario `CustomUserLoginForm`. Mediante el metodo POST recibe los datos entregados por el usuario mediante el formulario `CustomUserLoginForm`, valida los datos y los registra en la base de datos, adicionalmente crea una sessión de login con los datos del usuario recién registrado. Además, redirige a la vista que se haya configurado. De existir un problema rederizará el template con el fomulario de registro para repetir la operación e indicando los errores posibles.


```python
    CustomUserLoginView(LoginView):
        template_name = 'login.html'  
        form_class = CustomUserLoginForm
```
* Permite iniciar sesión al usuario, se ha personalizado el template que renderiza la vista y el formulario a mostrar.


```python
    @method_decorator(login_required, name='dispatch' )
```
* `@method_decorator` permite aplicar el decorador `login_required` al metodo 'dispatch', este último es parte del ciclo de vida de la vista, a fin de proteger la vista de quienes no hayan iniciado sesión de usuario.


```python
    class CustomPasswordChangeView(PasswordChangeView):
        template_name = 'change_password.html'
        form_class = CustomChangePasswordForm
```
* La vista renderiza el tempalte con el fomulario necesario para realizar el cambio de contraseña, solicita la contraseña actual, la nueva y repetir esta última.


```python
    class CustomPasswordChangeDoneView(PasswordChangeDoneView):
        def get(self, *args, **kwargs):
            return redirect('logout')
```
* La vista redirige a una vista y template determinada una vez realizado el cambio de contraseña. En este caso cierra la sesión del usuario y es redirigido a la pagina principal para que inicie sesión con la nueva contraseña.


```python
    def password_reset_request(request):
```
*  La vista se encaga de solicitar el email del usuario y enviar un correo con las instrucciones para reestablecer su contraseña.
    
    ```python
         if request.method == 'POST':
    ```
    * Verifica si la solicitud utilza el método `POST`, indicando que se está recibiendo información por parte del cliente y que se deben realizar acciones con los datos enviados.

    ```python
        password_form = PasswordResetForm(request.POST)
    ```
    * Crea un formulario con los datos enviados por el cliente.
    
    ```python
        if password_form.is_valid():
    ```
    * Verifica si el formulario es valido.

    ```python
        data = password_form.cleaned_data['email']
    ```
    * Obtiene el email ingresado en el formulario.

    ```python
        user_email = CustomUser.objects.filter(Q(email=data))
    ```
    * Busca y filtra desde la base de datos aquellos usuarios que tengan el email proporcionado en el formulario.

    ```python
        if user_email.exists():
    ```
    * Condiciona si exite un usuario con dicho corro electrónico, de exisitr, se ejecutara la lógica para enviar el email para el reestablecimiento de contraseña.
    
    ```python
        for user in user_email:
    ```
    * Itera sobre los usuarios encontrados con el filtro por email, nuestro modelo establese el campo como único, por tanto siempre debiese haber un email diferente por usuario. Pero el bucle puede servirte como ejemplo para otro tipos de lógica.

    ```python
        subject = "Reestablecimiento de contraseña"
    ```
    * Establece el asunto que se mostrará en nuestro email a enviar.

    ```python
        email_template_name = 'user_manager/password_reset_message.html'
    ```
    * Establece la plantilla `html` o `txt` que conformarán el cuerpo de nuestro email de reestablecimiento de contraseña.

    ```python
        parameters = {
            'site_name': 'Preset web App',
            'email': user_email,
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(uspk)),
            'token': default_token_generator.make_to(user),
            'fullname': user.full_name
        }
    ```
    * Declara los parametros que se utilizarán en la platilla para el correo electrónico, su contexto, `site_name` el nombre de nuestro sitio con el que nos identificaremos en el correo enviado, `fullname` el nombre de nuestro usuario para individualizarlo, `email` establece la dirección de correo electrónico del destinatario. Las siguientes claves permitirán construir el enlace para que el usuario pueda reestablecer la contraseña, `protocol`, es el protocolo que utilizataremos en nustra url, `domain` el dominio de nuestra aplicación en este caso `localhost`, `uid` representa el `id` del usuario con el cual estamos trabajando y quien a solicitado el reestablecimiento de contraseña, `urlsafe_base64_encode` toma una secuencia de bytes y la codifica en una versión segura para ser utilizada en una url,  `force_bytes` fuerza la conversión del id obtenido en una cadena de bytes para poder trabajar con ella, `user.pk` representa al id del usuario destinatario; `token` alamacena un token de identificación generado por `default_token_generator.make_token(user)` permitiendo un grado mayor de seguridad, de identificación y con expiración una vez utilizado el enlace.

    ```python
        <a href="{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}">Reestablecer contraseña</a>
    
    ```
    * Ejemplo del link que se debe generar en el template del correo electrónico con los datos antes mencionados

    ```python
        email_content = render_to_string(email_template_name, parameters)
    ```
    * Renderiza el contenido html en el email, se le envia como parametro el template y su contexto a utilizar.

    ```python
          email= EmailMessage(
                            subject=subject,
                            body=email_content,
                            to=[user.email]
                        )
    ```
    * Crea una instancia de `EmailMessage` entregando como argumento a su constructor el asunto, el cuerpo y destinarario.

    ```python
        try:
            email.send(fail_silently=False)
        except:
            return HttpResponse('Invalid Header')
        return redirect('password_reset_done') 
    ```
    * Intentaremos enviar nuestro email, por defecto email.send() no levanta ningún tipo de excepción ante fallos, con el parametro `fail_silently=False` hacemos que levante una excepción en caso de algun error,  de no poder enviar el email se generará una respuesta http con un mensaje. Finalmente, si ha salido todo bien y el email ha sido enviado. redireccionará a la vista `password_reset_done`.

    ```python
         else:
            password_form = PasswordResetForm()

         context = {
             'password_form': password_form
         }
         return render(request,'user_manager/password_resethtml',   context)
    ```
    * En caso de que la petición no sea con el metodo `POST` se renderizará `user_manager/password_reset.html` con el formulario de reestablecimiento de contraseña en su contexto.


```python
    class CustomPasswordResetDoneView(PasswordResetDoneView):
```
* La vista muestra un mensaje confirmando el envío de un correo electrónico con las instrucciones para cambiar la contraseña. 


```python
    class CustomPasswordResetConfirmView(PasswordResetConfirmView)
```
* La vista permite acceder al formulario por defecto para ingresar una nueva contraseña, la conexión se crea a traves de un token de seguridad, por tanto, el enlace proporcionado en el correo solo funcionará una vez. Si el token ha caducado se mostrara un mensaje explicando la situación, y debe repetir el proceso para el reestablecimiento de contraseña.


```python
    class CustomPasswordResetCompleteView(PasswordResetCompleteView):
```
* La vista se encarga de rendirizar un template con un mensaje indicando que el reestablecimiento de contraseña ha sido existos, acompañado de un link a la vista de login. 



## Rutas `urls.py`

* Se ecneuntra las urls a todas las vistas que se han personalizado

## Configuración general 
### `settings.py`

```python
    AUTH_USER_MODEL = 'user_manager.CustomUser'
```
* Determina el modelo que se ocupará para autenticarse en la aplicación como usario.


```python
    LOGIN_URL = 'login'
```
* Indica la ruta de `login`, se utiliza para redirigir a esta vista cuando se intenta acceder a una ruta protegida.


```python
    LOGIN = 'login'
```
* Determina que `login` es la vista determinada para realizar el inicio de sesión.

```python
    LOGIN_REDIRECT_URL = 'user_home'
    LOGOUT_REDIRECT_URL = 'user_home'
```
* Configura la ruta a la cual se redirigirá una vez se haya iniciado o cerrado sesión.


* ### `apps.py`

* Se ha agregado la variable `verbose_name` en la clase `class UserManagerConfig(AppConfig)` para dar un aspecto más homogéneo en el panel de administación de Django.

* ### `admin.py`
```python
    admin.site.site_header = 'PRESET WEB APPS'
    admin.site.site_title =  'preset web apps'
    admin.site.index_title = 'Panel de administración'

```
* Establece títulos personalizados para el panel de administración de Django.


```python
    class CustomUserAdmin(UserAdmin):
```
* Define una nueva clase llamada CustomUserAdmin que hereda de la clase UserAdmin. Esto extiende y personaliza la funcionalidad proporcionada por el administrador de usuarios predeterminado de Django.


```python
    list_display = ('email', 'full_name', 'is_active', 'is_staff')
```
* Especifica qué campos se deben mostrar en la lista de usuarios en la interfaz de administración.


```python
    search_fields = ('email', 'full_name')
```
* Especifica los campos por los cuales se puede realizar una búsqueda en la interfaz de administración.


```python
    readonly_fields = ('date_joined',)
```
* Indica que el campo date_joined (fecha de registro) es de solo lectura en la interfaz de administración.


```python
    ordering = ['email']
```
*


```python
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions'), 'classes': ('collapse',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
```
* Define los conjuntos de campos que se mostrarán y cómo se organizarán en la interfaz de administración al ver/editar un usuario.


```python
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2', 'full_name', 'country', 'is_active', 'is_staff')}
        ),
    )
```
* Define los conjuntos de campos que se mostrarán y cómo se organizarán en la interfaz de administración al agregar un nuevo usuario.


```python
    admin.site.register(CustomUser, CustomUserAdmin)
```
* Registra el modelo CustomUser y el administrador personalizado CustomUserAdmin en el sitio de administración de Django.


### Nota 
* La carpeta `templates/user_manager` tiene los templates a modo de ejemplos, modificalos según tus necesidades.
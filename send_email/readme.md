# Email Sender App

Esta es una aplicación simple en Django para enviar correos electrónicos utilizando la funcionalidad incorporada de en el framework para el envío de emails. 


>[!NOTA]
    La configuración esta realizada para uso con Gmail.

# Instrucciones

1. Clone el repositorio o descarge la carpeta send_email.
2. Copie la carpeta send_email en su proyecto.
3. Incluya la url de su aplicación a las urls de su proteyecto.
4. En settings.py de su proyecto incluya las siguientes variables, modficando los valores por sus credenciales.
    ```python
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'remitente@gmail.com'
    EMAIL_HOST_PASSWORD = 'Contraseña de aplicación otorgada por google'
    ```

>[!TIP]
    ### Para obtener la contraseña de aplicación
    * Inicie sesión en su cuenta gmail, la cuenta debe coincidir con su mail configurado en la variable `EMAIL_HOST_USER` setting.py.
        ```python
        EMAIL_HOST_USER = 'remitente@gmail.com'
        ```

    * Ingrese a [Configuración de cuenta google](https://myaccount.google.com/)

    * Ve a la sección de seguridad, cuando estés allí, en la sección de búsqueda en la esquina superior izquierda, escribe "Contraseña  de aplicación", e ingresa a la opción. Para poder ingresar a la opción y que todo resulte correctamente debes tener activa la    verificación de dos paso de la cuenta gmail utilizada como `EMAIL_HOST_USER` en tu settings.py.

    * Te pedirá ingresar la contraseña de tu cuenta.

    * Cree un app name haciendo referencia a tu aplicación Django. haz click en crear.

    * Aparecerá un cuadro de diálogo con su contraseña de aplicación. copiela y de click en hecho.

    * Pegue la contraseña brindadac en la variable `EMAIL_HOST_PASSWORD`configurada en settings.py reemplazando el valor de la  variable por su contraseña de aplicación generada.
        ```python
        EMAIL_HOST_PASSWORD = 'Contraseña de aplicación otorgada por google'
        ```

5. Configure el views.py de acuerdo a sus necesidades reemplazando los campos de las variables y generando la lógica necesaria.
 ```python
    def send_email(request):
        if request.method == 'POST':
            informacion = "¡Hola! Este es el contenido del correo."
            destinatario = 'destinatario@gmail.com'
            asunto = 'Prueba'
            remitente = 'remitente@gmail.com'
            send_mail(asunto, informacion, remitente, [destinatario])
            return redirect('send_email')

        return render(request, 'send_email.html') 
 ```
>[!CAUTION]
    ## Sobre la seguridad de tus datos y credenciales
    * Si llevarás tu proyecto a producción o lo compartiras con terceros recuerda nunca colocar tus credenciales en el código, utiliza variables de entorno para mantener la privacidad de tus credenciales.

* ### Sugerencia de uso de dotenv para manejar tus variables de entorno

* Desde la terminal ejecuta `pip install python-dotenv`.

* Crea un archivo en la raiz de tu proyecto, a la altura del manage.py y nombralo ".env", dentro del escribiras tus variables de entorno siguiendo este ejemplo:
 ```python
    #Django
    SECRET_KEY=llave que se encuentra en tu setting.py con el mismo nombre de variable.

    # send_email variables
    #settings.py
    EMAIL_HOST_PASSWORD=clave dada por gmail
    EMAIL_HOST_USER=remitente@gmail.com
    #views.py
    DESTINATARIO=destinatario@gmail.com
    REMITENTE=remitente@gmail.com  
 ```
* Recueda los valores en las variables se escriben sin comillas, incluso si el valor a almacenar es una cadena., y tanto el nombre de la varable, el signo = y el valor se escribe sin espacios entre ellos.

* Luego, en los archivos.py que necesite importar las variables añade lo siguiente:
 ```python
    from dotenv import load_dotenv
    import os
    load_dotenv()
 ```
*El código en tus archivos.py donde hará uso de las variables de entorno debe verse así:
 ```python
    #settings.py
    EMAIL_HOST_USER = os.getenv('REMITENTE')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    #views.py
    destinatario = os.getenv('DESTINATARIO') #Ej: correodeldestinatario@gmail.com
    remitente = os.getenv('REMITENTE') #Ej: micorreo@gmail.com
 ```

 * Asegurate de crear tu archivo .gitignore y añadir .env en él. 
 
## Contribución
¡Contribuciones son bienvenidas! Si encuentras algún problema o tienes ideas para mejorar la aplicación, sigue estos pasos:

Crea un nuevo issue explicando el problema o la mejora.
Haz un fork del repositorio.
Crea una nueva rama para tu contribución: git checkout -b feature/nueva-funcion
Realiza los cambios y haz commit: git commit -m "Añadir nueva función"
Haz push a tu rama: git push origin feature/nueva-funcion
Crea un pull request en GitHub.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

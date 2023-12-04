# Email Sender App

Esta es una aplicación simple en Django para enviar correos electrónicos utilizando la funcionalidad incorporada de Django para el envío de emails. 

### Nota

La configuracion esta realizada para uso con Gmail.

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
### Nota
* Para obtener la contraseña de aplicación ingrese a [Configuracion](https://accounts.google.com/v3/signin/challenge/pwd?TL=AHNYTITaPTH_fYldMiqikAcpzSFYiobVuWXQZNga1D8SZiVHl0KI79RTYjGS1_gN&cid=2&continue=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords%3Fpli%3D1%26rapt%3DAEjHL4OQcNIu2htsuypNiVCH3N_ABixglnphVcH2LzpWEjshLk0nZbTA9EKfouQdU-rKTU7mwgKm7yaUjI3WXv2sX6eloumQ5A4492hboG0BsLg4BRw7OWo&flowName=GlifWebSignIn&ifkv=ASKXGp3FADtLpNmkIiYu0O0N95YeamgnoIUULUFUbeCiUS8Noc5eMoisKL9TSk4mw74M9rKET8h7_A&rart=ANgoxcdCt9h4nfhSwrQkEwHrSyuaOOVjbs2MWMuEsgQCXFBz3B58mu1ttmfyibcwc3TmYK68DMknMuJ7N7BPOX4zfsWbpJxepQohP_fhyUsPHmyp88CAQDA&rpbg=1&sarp=1&scc=1&service=accountsettings&theme=glif)

* Inicie sesión este debe coincidir con su mail configurado en settings.py reemplazando el valor de la variable.
    ```python
    EMAIL_HOST_USER = 'remitente@gmail.com'
    ```
* Cree un app name haciendo referencia a su aplicacion Django

* Aparecerá un cuadro de diálogo con su contraseña copiela y de click en hecho.

* Pegue la contraseña brindada password configurada en settings.py reemplazando el valor del a variable.
    ```python
    EMAIL_HOST_PASSWORD = 'Contraseña de aplicación otorgada por google'
    ```

5. Configure el archivo.py de acuerdo a sus necesidades reemplazando los campos de las variables y generando la lógica necesaria.
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

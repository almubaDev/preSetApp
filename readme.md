# preSetApp

## Bienvenido a preSetApp

preSetApp es una iniciativa diseñada para simplificar el desarrollo de aplicaciones con el framework Django. Este proyecto ofrece una colección de aplicaciones prácticas que resuelven tareas comunes. Puedes integrar estas aplicaciones en tus proyectos para acelerar tu desarrollo y aprender sobre las configuraciones y la inicialización necesarias para cada solución específica.

## Objetivo

El objetivo principal de preSetApp es proporcionar recursos prácticos para aquellos que están aprendiendo Django. Queremos facilitar el acceso a soluciones para problemas comunes y fomentar la comprensión de las configuraciones necesarias para integrar estas aplicaciones en sus propios proyectos.

## Aplicaciones Disponibles

Actualmente, preSetApp incluye las siguientes aplicaciones:

- **Email Sender App:** Una aplicación simple que utiliza la funcionalidad de envío de correos electrónicos de Django. Ideal para configurar y enviar correos electrónicos desde tu aplicación.

    [Enlace a la Documentación de Email Sender App](https://github.com/almubaDev/preSetApp/tree/main/send_email)

(Más aplicaciones pueden ser agregadas en el futuro).

## Por seguridad recuerda crear tus variables de entorno y hacer las modificaciones necesarías para correr las aplicaciones.
* ### Sugerencia de uso de dotenv para manejar tus variables de entorno

* Desde la terminal ejecuta `pip install python-dotenv`.

* Crea un archivo en la raiz de tu proyecto, a la altura del manage.py y nombralo ".env" y escribe en el las varibales de entorno que deseas utilizar, sigue este ejemplo:
 ```python
    MI_CLAVE_SUPER_SECRETA=fsdfsdfsdf242345234534#d)))$!#"#!
    #Recuerda no generar espacios entre el nombre de la variable, el signo = y el valor.
    #El valor deber ir sin comillas ni al inicio ni al final, incluso si el valor a almacenar es una cadena.
 ```

* En tu archivo.py donde necesite usar la variable escribe: 
 ```python
    from dotenv import load_dotenv
    import os
    load_dotenv()

    MY_PASSWORD = os.getenv('MI_CLAVE_SUPER_SECRETA')
 ```
 * Asegurate de crear tu archivo .gitignore y añadir .env en él. 

## Contribuciones

¡Contribuciones son bienvenidas! Si deseas agregar nuevas aplicaciones, mejorar la documentación, o realizar correcciones, por favor, abre un problema o envía una solicitud de extracción.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

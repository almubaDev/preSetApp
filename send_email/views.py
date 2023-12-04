from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os

from django.core.mail import send_mail

load_dotenv()
#Una vez lleves la aplicación a tu proyecto adapta la lógica según tus necesidades, así como la conexión a las templates correspondientes.
def send_email(request):
    if request.method == 'POST':
        informacion = "¡Hola! Este es el contenido del correo."
        destinatario = os.getenv('DESTINATARIO') #Ej: correodeldestinatario@gmail.com
        asunto = 'Prueba'
        remitente = os.getenv('REMITENTE') #Ej: micorreo@gmail.com
        send_mail(asunto, informacion, remitente, [destinatario])
        return redirect('send_email')

    return render(request, 'send_email.html')


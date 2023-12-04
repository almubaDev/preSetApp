from django.shortcuts import render, redirect
from django.core.mail import send_mail

def send_email(request):
    if request.method == 'POST':
        informacion = "¡Hola! Este es el contenido del correo."
        destinatario = 'destinatario@gmail.com'
        asunto = 'Prueba'
        remitente = 'remitente@gmail.com'
        send_mail(asunto, informacion, remitente, [destinatario])
        return redirect('send_email')

    return render(request, 'send_email.html')


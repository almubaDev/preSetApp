from django.shortcuts import render
from .forms.forms import PasswordGeneratorForm
import string
import random





def password_generator(request):
    if request.method == 'POST':
        data = request.POST.get('cant', 4)
        include_uppercase = request.POST.get('include_uppercase')
        include_lowercase = request.POST.get('include_lowercase')
        include_digit = request.POST.get('include_digit')
        include_special_char = request.POST.get('include_special_char')

        characters = ''

        if include_uppercase:
            characters += string.ascii_uppercase

        if  include_lowercase:
            characters += string.ascii_lowercase

        if include_digit:
            characters +=  string.digits

        if include_special_char:
            characters += string.punctuation
        
        # if not characters:
        #     characters = ' '

        password = ''
        try:
            for i in range(int(data)):
                char = random.choice(characters)
                password += char 

            return render(request, 'password_generator/password_generator.html',{'password': password})
        
        except IndexError:
            return render(request, 'password_generator/password_generator.html', {'error': 'Seleccione al menos un tipo de caracter a considerar en su contraseña.'})

        except ValueError:
                        return render(request, 'password_generator/password_generator.html', {'error': 'Debe ingresar un número valido para la cantida de caracteres que tendrá su contraseña.'})
    return render(request, 'password_generator/password_generator.html')
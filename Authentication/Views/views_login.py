from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate,logout
from Authentication.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from Authentication.models import PasswordResetCode, CustomUser
from django.contrib.auth.hashers import make_password
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.hashers import make_password

User = get_user_model()

def home_view(request):
    return render(request, 'core/Home.html')

        
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'core/Authentication/signup.html', {'form': form})
    else:
        return render(request, 'core/Authentication/signup.html', {'form': CustomUserCreationForm()})

def signin_view(request):
    if request.method == 'GET':
        return render(request, 'core/Authentication/signin.html',{
        'form': AuthenticationForm()
    })  
    else :
        user = authenticate(request, username=request.POST['username'], password=request.POST
                     ['password'])
        if user is None:
            return render(request, 'core/Authentication/signin.html',{
            'form': AuthenticationForm(),
             'error': 'Usuario o contraseña incorrectos o no existen.'})
            
        else:
            login(request, user)
            return redirect('inicio')
   
def logout_view(request):
    logout(request)
    return redirect('home')
                                               


def request_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            code = f"{random.randint(100000, 999999)}"      
            PasswordResetCode.objects.create(user=user, code=code)
            send_verification_email(user_email=email, verification_code=code)
            return render(request, 'core/password_reset/code_sent.html')  
    return render(request, 'core/password_reset/request_reset.html')


def verify_code_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        user = CustomUser.objects.filter(email=email).first()
        if user:
    
            record = PasswordResetCode.objects.filter(user=user, code=code).last()
         
            if record and record.is_valid():
                request.session['reset_user_id'] = user.id
                return redirect('set_new_password')  
        return render(request, 'core/password_reset/verify_code.html', {'error': 'Código incorrecto o expirado.'})
    return render(request, 'core/password_reset/verify_code.html')


def set_new_password_view(request):
    user_id = request.session.get('reset_user_id')
    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        return redirect('password_reset_custom')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
          
            user.password = make_password(password1)
            user.save()
            del request.session['reset_user_id']
            return redirect('signin')  
        else:
            return render(request, 'core/password_reset/set_new_password.html', {'error': 'Las contraseñas no coinciden.'})

    return render(request, 'core/password_reset/set_new_password.html')


def send_verification_email(user_email, verification_code):
    subject = 'Tu código de verificación - MODAMIND'

    html_message = render_to_string(
        'core/password_reset/emails/verification_email.html',  
        {
            'verification_code': verification_code,
            'app_name': 'MODAMIND'
        }
    )
    send_mail(
        subject=subject,
        message='Este es un mensaje de verificación. Si ves esto, tu cliente de correo no soporta HTML.',
        from_email=settings.DEFAULT_FROM_EMAIL,  
        html_message=html_message,  
    )


     
    
  
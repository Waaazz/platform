from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.messages import SUCCESS
from .tokens import account_activation_token

def login_blog(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['pwd']
            user = authenticate(username=username, password=pwd)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Authentification échouée")
                return render(request, 'login.html', {'form': form})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += 'is-invalid'
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd']
            pwd_confirmation = form.cleaned_data['pwd_confirmation']

            # Vérification de la correspondance des mots de passe
            if pwd != pwd_confirmation:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, 'register.html', {'form': form})

            # Vérification si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur existe déjà.")
                return render(request, 'register.html', {'form': form})

            # Création de l'utilisateur mais pas encore activé
            user = User.objects.create_user(username=username, email=email, password=pwd)
            user.is_active = False
            user.save()
            
            # Générer le lien de confirmation
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            confirmation_link = reverse('confirm-registration', kwargs={'uidb64': uid, 'token': token})

            # Rendre le modèle HTML avec le contexte approprié
            message = render_to_string('confirmation_email.html', {
                'user': user,
                'confirmation_link': request.build_absolute_uri(confirmation_link),
            })

            # Envoi de l'e-mail
            send_mail(
                'Confirmation d\'inscription',
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return render(request, 'registration_success.html', {'user': request.user})  # Passer le nom d'utilisateur au contexte
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
def confirm_registration(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request,SUCCESS, 'Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter.')
        return redirect('login-blog')
    else:
        messages.error(request, 'Le lien d\'activation est invalide ou a expiré.')
        return redirect('login-blog')
    
def logout_blog(request):
    logout(request)
    return redirect('login-blog')

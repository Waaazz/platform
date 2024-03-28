from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    # Définir les messages d'erreur personnalisés
    error_messages = {
        'required': "Ce champ est requis.",
    }

    # Mettre à jour les paramètres du formulaire pour utiliser les messages d'erreur personnalisés
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = self.error_messages

class RegisterForm(forms.Form):
    username = forms.CharField(label="Nom utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Adresse e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    pwd_confirmation = forms.CharField(label="Mot de passe de confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()  # Champ reCAPTCHA
    # Définir les messages d'erreur personnalisés
    error_messages = {
        'required': "Ce champ est requis.",
    }

    # Mettre à jour les paramètres du formulaire pour utiliser les messages d'erreur personnalisés
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = self.error_messages

    # Ajouter la classe CSS personnalisée aux messages d'erreur
    def add_error(self, field, error):
        super().add_error(field, error)
        if field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control is-invalid'}) # Mettre à jour la classe du champ avec la classe is-invalid pour que le message d'erreur soit affiché en rouge

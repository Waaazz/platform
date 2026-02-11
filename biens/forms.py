from django import forms
from .models import Article, UserProfile, Message
from django.utils import timezone


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'category', 'description', 'image1', 'image2', 'image3', 'image4', 'prix', 'disponible']
        labels = {
            'nom': 'Nom du bien',
            'category': 'Categorie',
            'description': 'Description',
            'disponible': 'Disponible',
            'prix': 'Prix par jour (FCFA)',
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du bien'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Decrivez votre bien...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReservationForm(forms.Form):
    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )
    telephone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+221 XX XXX XX XX'})
    )
    date_checkin = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date d'arrivee"
    )
    date_checkout = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date de depart"
    )
    modalites_paiement = forms.ChoiceField(
        choices=[
            ('especes', 'Especes'),
            ('virement', 'Virement bancaire'),
            ('mobile_money', 'Mobile Money'),
            ('paypal', 'PayPal'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Mode de paiement"
    )

    def clean(self):
        cleaned_data = super().clean()
        checkin = cleaned_data.get('date_checkin')
        checkout = cleaned_data.get('date_checkout')
        if checkin and checkout:
            if checkout <= checkin:
                raise forms.ValidationError("La date de depart doit etre apres la date d'arrivee.")
            if checkin < timezone.now().date():
                raise forms.ValidationError("La date d'arrivee ne peut pas etre dans le passe.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['telephone', 'adresse', 'ville', 'avatar', 'bio']
        widgets = {
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ecrivez votre message...'
            }),
        }

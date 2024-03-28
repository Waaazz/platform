from django import forms 
from .models import Article,Reservation

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['nom','category','description','image1','image2','image3','image4','prix','disponible']
        labels = {'nom':'nom','category':'Categorie','description':'description', 'disponible': 'Disponible'}
        widgets = {
            'nom':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':5}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class ReservationForm(forms.Form):
    nom = forms.CharField(max_length=100)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=20) 
    modalites_paiement = forms.CharField(max_length=100)
    

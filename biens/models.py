from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Article(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    nom = models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField()
    image1 = models.ImageField(upload_to='article_images', null=True, blank=True)
    image2 = models.ImageField(upload_to='article_images', null=True, blank=True)
    image3 = models.ImageField(upload_to='article_images', null=True, blank=True)
    image4 = models.ImageField(upload_to='article_images', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse("my-articles")
    
    def is_available(self):
        return self.disponible
    
    def can_reserve(self):
        return self.disponible
    
    def reserve(self):
        if self.is_available():
            self.disponible = False
            self.save()
    
            
class Reservation(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    prix_article = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_reservation = models.DateTimeField(default=timezone.now)
    modalites_paiement = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Reservation {self.id} - {self.article.nom}"



class Note(models.Model):
    article = models.ForeignKey(Article, related_name='notes', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Ajout d'une valeur par défaut None
    note = models.IntegerField(default=1)
    commentaire = models.TextField(default="Aucun commentaire")

    def __str__(self):
        return f"Note {self.id} - {self.article.nom} - Utilisateur: {self.utilisateur.username}"
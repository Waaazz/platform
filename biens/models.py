from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image1 = models.ImageField(upload_to='article_images', null=True, blank=True)
    image2 = models.ImageField(upload_to='article_images', null=True, blank=True)
    image3 = models.ImageField(upload_to='article_images', null=True, blank=True)
    image4 = models.ImageField(upload_to='article_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    STATUT_CHOICES = [
        ('confirmee', 'Confirmee'),
        ('annulee', 'Annulee'),
        ('terminee', 'Terminee'),
    ]
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    prix_article = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_checkin = models.DateField(null=True, blank=True)
    date_checkout = models.DateField(null=True, blank=True)
    date_reservation = models.DateTimeField(default=timezone.now)
    modalites_paiement = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='confirmee')

    def __str__(self):
        return f"Reservation {self.id} - {self.article.nom}"

    def duree_jours(self):
        if self.date_checkin and self.date_checkout:
            return (self.date_checkout - self.date_checkin).days
        return 0

    def calculer_prix_total(self):
        jours = self.duree_jours()
        if jours > 0:
            return self.prix_article * jours
        return self.prix_article


class Note(models.Model):
    article = models.ForeignKey(Article, related_name='notes', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    note = models.IntegerField(default=1)
    commentaire = models.TextField(default="Aucun commentaire")

    def __str__(self):
        return f"Note {self.id} - {self.article.nom} - {self.utilisateur.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone = models.CharField(max_length=20, blank=True, default="")
    adresse = models.CharField(max_length=255, blank=True, default="")
    ville = models.CharField(max_length=100, blank=True, default="")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} - {self.article.nom}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"De {self.sender.username} a {self.receiver.username}"

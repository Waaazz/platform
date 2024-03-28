# Generated by Django 4.2.7 on 2024-02-27 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('biens', '0018_remove_article_avis_remove_article_notation_moyenne'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='valeur',
        ),
        migrations.AddField(
            model_name='note',
            name='commentaire',
            field=models.TextField(default='Aucun commentaire'),
        ),
        migrations.AddField(
            model_name='note',
            name='note',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='note',
            name='utilisateur',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
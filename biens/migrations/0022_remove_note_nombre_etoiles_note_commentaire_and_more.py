# Generated by Django 4.2.7 on 2024-03-12 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('biens', '0021_remove_note_commentaire_note_nombre_etoiles_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='nombre_etoiles',
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
        migrations.AlterField(
            model_name='note',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='biens.article'),
        ),
        migrations.AlterField(
            model_name='note',
            name='utilisateur',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Commentaire',
        ),
    ]
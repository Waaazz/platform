# Generated by Django 4.2.7 on 2024-02-26 21:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0015_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='date_reservation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='reservation',
            name='modalites_paiement',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='prix_article',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

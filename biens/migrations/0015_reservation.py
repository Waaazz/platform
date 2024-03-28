# Generated by Django 4.2.7 on 2024-02-26 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0014_remove_article_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=20)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biens.article')),
            ],
        ),
    ]
# Generated by Django 4.2.7 on 2024-03-18 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0003_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]

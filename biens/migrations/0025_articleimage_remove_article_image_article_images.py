# Generated by Django 4.2.7 on 2024-03-22 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0024_delete_articleimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='article_images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.AddField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='articles', to='biens.articleimage'),
        ),
    ]

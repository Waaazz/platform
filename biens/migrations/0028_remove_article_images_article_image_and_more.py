# Generated by Django 4.2.7 on 2024-03-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0027_remove_article_image_articleimage_article_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='images',
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='ArticleImage',
        ),
    ]

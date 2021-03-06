# Generated by Django 3.2.7 on 2021-10-22 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_auto_20211022_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='contact_pics'),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]

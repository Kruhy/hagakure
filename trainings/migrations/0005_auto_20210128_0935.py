# Generated by Django 2.2.16 on 2021-01-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0004_trainerbio_disciplines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainerbio',
            name='photo',
            field=models.ImageField(default='img/no-avatar.png', upload_to='img/trainers'),
        ),
    ]

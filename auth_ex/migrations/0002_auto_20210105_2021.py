# Generated by Django 2.2.17 on 2021-01-05 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_ex', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True),
        ),
    ]

# Generated by Django 3.2 on 1980-01-01 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekereapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_email',
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]

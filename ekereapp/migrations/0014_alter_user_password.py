# Generated by Django 3.2 on 1980-01-01 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekereapp', '0013_auto_20220309_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]

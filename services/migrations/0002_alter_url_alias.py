# Generated by Django 4.2.7 on 2023-11-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='alias',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]

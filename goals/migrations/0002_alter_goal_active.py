# Generated by Django 3.2.24 on 2024-03-08 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

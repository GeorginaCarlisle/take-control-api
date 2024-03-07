# Generated by Django 3.2.24 on 2024-03-07 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
                ('colour', models.CharField(choices=[('fuchsia', 'Fuchsia'), ('lime', 'Lime'), ('yellow', 'Yellow'), ('aqua', 'Aqua'), ('aquamarine', 'Aquamarine'), ('gold', 'Gold'), ('lightsalmon', 'Light Salmon'), ('orange', 'Orange'), ('orangered', 'Orange Red'), ('pink', 'Pink'), ('plum', 'Plum'), ('skyblue', 'Sky Blue')], max_length=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='label', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

from django.db import models
from django.contrib.auth.models import User

colour_choices = [
    ("fuchsia", "Fuchsia"),
    ("lime", "Lime"),
    ("yellow", "Yellow"),
    ("aqua", "Aqua"),
    ("aquamarine", "Aquamarine"),
    ("gold", "Gold"),
    ("lightsalmon", "Light Salmon"),
    ("orange", "Orange"),
    ("orangered", "Orange Red"),
    ("pink", "Pink"),
    ("plum", "Plum"),
    ("skyblue", "Sky Blue")]

class Label(models.Model):
    """
    Label model
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="label")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20)
    colour = models.CharField(choices=colour_choices, max_length=20)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'

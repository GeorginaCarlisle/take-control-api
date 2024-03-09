from django.db import models
from django.contrib.auth.models import User


class Focus(models.Model):
    """
    Focus model
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="focus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    rank = models.IntegerField(blank=True, null=True)
    why = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', default='../default-focus_bpca53', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'

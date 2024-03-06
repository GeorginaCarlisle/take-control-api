from django.db import models
from django.contrib.auth.models import User
from focus.models import Focus


class Goal(models.Model):
    """
    Goal model
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="goal")
    focus = models.ForeignKey(
        Focus,
        on_delete=models.CASCADE,
        related_name="goal_for_focus")
    children = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="nested_goal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    criteria = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'

from django.db import models
from django.contrib.auth.models import User
from focus.models import Focus
from goals.models import Goal
from labels.models import Label


class Task(models.Model):
    """
    Task model
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="task")
    focus = models.ForeignKey(
        Focus,
        on_delete=models.CASCADE,
        related_name="task_for_focus",
        blank=True,
        null=True)
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="task_for_goal",
        blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    today = models.BooleanField(default=False)
    achieved = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    deadline = models.DateTimeField(null=True, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'

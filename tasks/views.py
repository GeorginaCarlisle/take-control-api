from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, filters
from take_control_api.permissions import OwnerOnly


class TaskList(generics.ListCreateAPIView):
    """
    View to return a list of tasks for the logged in user
    and also to create a new task
    """
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        """
        Adds owner data to the object before it is saved
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Pulls all of the task instances that are owned by the user
        and only those owned by the user. Within this order by
        deadline and then created_by
        """
        return self.request.user.task.all().order_by('created_at')
from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, filters
from take_control_api.permissions import OwnerOnly


class ListFilter(filters.BaseFilterBackend):
    """
    Custom filter to filter the task list by:
    active, today
    """
    def filter_queryset(self, request, queryset, view):
        active = request.query_params.get('active')
        if active == 'True':
            queryset = queryset.filter(active=True)
        elif active == 'False':
            queryset = queryset.filter(active=False)
        today = request.query_params.get('today')
        if today == 'True':
            queryset = queryset.filter(today=True)
        elif today == 'False':
            queryset = queryset.filter(today=False)
        achieved = request.query_params.get('achieved')
        if achieved == 'True':
            queryset = queryset.filter(achieved=True)
        elif achieved == 'False':
            queryset = queryset.filter(achieved=False)
        return queryset

class TaskList(generics.ListCreateAPIView):
    """
    View to return a list of tasks for the logged in user
    and also to create a new task
    """
    serializer_class = TaskSerializer
    filter_backends = [
        ListFilter
    ]

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
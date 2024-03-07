from .models import Goal
from .serializers import GoalSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
#from take_control_api.permissions import OwnerOnly


class ParentFilter(filters.BaseFilterBackend):
    """
    Custom filter to filter goal list to include only goals with no parent
    """
    def filter_queryset(self, request, queryset, view):
        parent_id = request.query_params.get('parent_id')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        else:
            queryset = queryset.filter(parent=None)
        return queryset


class GoalList(generics.ListCreateAPIView):
    """
    View to return a list of goals for the logged in user
    and also create a new goal
    """
    serializer_class = GoalSerializer
    filter_backends = [
        ParentFilter
    ]

    def perform_create(self, serializer):
        """
        Adds owner data to the object before it is saved
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Pulls all of the goal instances that are linked to the current user
        and only focus instances that are linked to the current user. Within
        this order by rank first (with null last), and then by created_at.
        """
        return self.request.user.goal.all().order_by('deadline', 'created_at')

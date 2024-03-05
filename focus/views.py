from django.shortcuts import render
from .models import Focus
from .serializers import FocusSerializer
from rest_framework import generics
from take_control_api.permissions import OwnerOnly


class FocusList(generics.ListCreateAPIView):
    """
    View to return an list of focus areas and 
    also create a new focus area
    """
    serializer_class = FocusSerializer

    def perform_create(self, serializer):
        """
        Adds owner data to the object before it is saved
        """
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """
        Pulls all of the focus instances that are linked to the current user
        and only focus instances that are linked to the current user.
        Within this order by rank first (with null last), and then by created_at.
        """
        return self.request.user.focus.all().order_by('rank', 'created_at')


class FocusDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to return a specific focus where pk will be the id of the post
    """
    serializer_class = FocusSerializer
    permission_classes = [OwnerOnly]
    queryset = Focus.objects.all()

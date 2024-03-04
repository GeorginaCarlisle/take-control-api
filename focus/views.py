from django.shortcuts import render
from .models import Focus
from .serializers import FocusSerializer
from rest_framework import generics


class FocusList(generics.ListCreateAPIView):
    """
    View to return an list of focus areas and 
    also create a new focus area
    """
    serializer_class = FocusSerializer
    queryset = Focus.objects.all()

    def perform_create(self, serializer):
        """
        Adds owner data to the object before it is saved
        """
        serializer.save(owner=self.request.user)


class FocusDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to return a specific focus where pk will be the id of the post
    """
    serializer_class = FocusSerializer
    queryset = Focus.objects.all()   


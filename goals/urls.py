from django.urls import path
from goals import views

urlpatterns = [
    path('goals/', views.GoalList.as_view()),
]

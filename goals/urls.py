from django.urls import path
from goals import views

urlpatterns = [
    path('goals/', views.GoalList.as_view()),
    path('goals/<int:pk>', views.GoalDetail.as_view()),
]

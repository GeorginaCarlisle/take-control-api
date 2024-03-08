from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.TaskList.as_view()),
    path('tasks/<int:pk>', views.TaskDetail.as_view()),
]

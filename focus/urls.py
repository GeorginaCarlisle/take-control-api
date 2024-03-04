from django.urls import path
from focus import views

urlpatterns = [
    path('focus/', views.FocusList.as_view()),
    path('focus/<int:pk>', views.FocusDetail.as_view()),
]
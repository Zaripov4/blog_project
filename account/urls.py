from django.urls import path
from .api import RegisterApi

urlpatterns = [
      path('register/', RegisterApi.as_view()),
]

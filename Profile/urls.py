from django.urls import path
from .views import current_user

urlpatterns = [
  path('usuario/', current_user),
]
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Cargo

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = (
      'username',
      'first_name',
      'last_name',
      'email',
      'last_login',
      'date_joined',
    )
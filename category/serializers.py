from rest_framework import serializers
from category.models import Category
from Profile.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Category
    fields = (
      'id',
      'name',
      'created_at',
      'last_update', 
      'process',
    )
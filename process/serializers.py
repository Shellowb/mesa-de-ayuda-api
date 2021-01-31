from rest_framework import serializers
from process.models import Process
from Profile.serializers import UserSerializer

class ProcessSerializer(serializers.ModelSerializer):

  class Meta:
    model = Process
    fields = [
      'id',
      'name',
      'description',
      'banner_description',
      'icon',
      'published',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    ]

class ProcessRetriveSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  updated_by = UserSerializer(read_only=True)

  class Meta:
    model = Process
    fields = [
      'id',
      'name',
      'description',
      'banner_description',
      'icon',
      'published',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    ]
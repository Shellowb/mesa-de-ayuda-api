from rest_framework import serializers
from instances.models import Instance, Steps, News
from Profile.serializers import UserSerializer

class InstanceSerializer(serializers.ModelSerializer):

  class Meta:
    model = Instance
    fields = (
      'id',
      'name',
      'published',
      'process',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    )

class InstanceRetriveSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  updated_by = UserSerializer(read_only=True)

  class Meta:
    model = Instance
    fields = (
      'id',
      'name',
      'published',
      'process',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    )

class StepsSerializer(serializers.ModelSerializer):

  class Meta:
    model = Steps
    fields = (
      'id',
      'start_date',
      'end_date',
      'name',
      'description',
      'instance',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    )

class StepsRetriveSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  updated_by = UserSerializer(read_only=True)

  class Meta:
    model = Steps
    fields = (
      'id',
      'start_date',
      'end_date',
      'name',
      'description',
      'instance',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    )

class NewsSerializer(serializers.ModelSerializer):

  class Meta:
    model = News
    fields = (
      'id',
      'description',
      'instance',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    )

class NewsRetriveSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  updated_by = UserSerializer(read_only=True)

  class Meta:
    model = News
    fields = (
      'id',
      'description',
      'instance',
      'created_at',
      'last_update',
      'created_by',
      'updated_by'
    )